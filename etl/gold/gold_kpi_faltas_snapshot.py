import getpass
from datetime import datetime

import pandas as pd  # type: ignore

from etl.utils.db_connection import get_connection
from etl.gcp.upload_bigquery import carregar_tabela_bigquery


conn = get_connection()
cursor = conn.cursor()

processo = "gold_kpi_faltas_snapshot"
tabela = "gold.kpi_faltas_snapshot"

data_inicio = datetime.now()
linhas_inseridas = 0

try:

    # =========================
    # AUDIT START
    # =========================
    cursor.execute("""
        INSERT INTO audit.etl_run_log (
            processo,
            tabela,
            status,
            data_inicio,
            usuario_execucao
        )
        VALUES (%s,%s,%s,%s,%s)
        RETURNING id
    """, (
        processo,
        tabela,
        "RUNNING",
        data_inicio,
        getpass.getuser()
    ))

    log_id = cursor.fetchone()[0]
    conn.commit()

    print("Iniciando GOLD Faltas Snapshot...")

    # =========================
    # GOLD POSTGRES
    # =========================
    cursor.execute("""
        INSERT INTO gold.kpi_faltas_snapshot (
            data_referencia,
            qtd_faltas_pacientes,
            qtd_faltas_terapeutas,
            sessoes_perdidas_pacientes,
            sessoes_perdidas_terapeutas,
            receita_perdida_total
        )

        SELECT
            COALESCE(fp.data_falta, ft.data_falta) AS data_referencia,

            COALESCE(fp.total_faltas, 0) AS qtd_faltas_pacientes,
            COALESCE(ft.total_faltas, 0) AS qtd_faltas_terapeutas,

            COALESCE(fp.sessoes_perdidas, 0) AS sessoes_perdidas_pacientes,
            COALESCE(ft.sessoes_perdidas, 0) AS sessoes_perdidas_terapeutas,

            COALESCE(fp.receita_perdida, 0) + COALESCE(ft.receita_perdida, 0)
            AS receita_perdida_total

        FROM (
            SELECT
                data_falta,
                COUNT(*) AS total_faltas,
                SUM(qtd_sessoes_perdidas) AS sessoes_perdidas,
                SUM(receita_perdida) AS receita_perdida
            FROM silver.faltas_pacientes
            GROUP BY data_falta
        ) fp

        FULL OUTER JOIN (
            SELECT
                data_falta,
                COUNT(*) AS total_faltas,
                SUM(qtd_sessoes_perdidas) AS sessoes_perdidas,
                SUM(receita_perdida) AS receita_perdida
            FROM silver.faltas_terapeutas
            GROUP BY data_falta
        ) ft
        ON fp.data_falta = ft.data_falta

        ON CONFLICT (data_referencia)
        DO UPDATE SET
            qtd_faltas_pacientes = EXCLUDED.qtd_faltas_pacientes,
            qtd_faltas_terapeutas = EXCLUDED.qtd_faltas_terapeutas,
            sessoes_perdidas_pacientes = EXCLUDED.sessoes_perdidas_pacientes,
            sessoes_perdidas_terapeutas = EXCLUDED.sessoes_perdidas_terapeutas,
            receita_perdida_total = EXCLUDED.receita_perdida_total
    """)

    linhas_inseridas = cursor.rowcount
    conn.commit()

    print("Gold faltas carregado no Postgres")

    # =========================
    # LOAD BIGQUERY
    # =========================
    cursor.execute("""
        SELECT
            data_referencia,
            qtd_faltas_pacientes,
            qtd_faltas_terapeutas,
            sessoes_perdidas_pacientes,
            sessoes_perdidas_terapeutas,
            receita_perdida_total
        FROM gold.kpi_faltas_snapshot
    """)

    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns=[
        "data_referencia",
        "qtd_faltas_pacientes",
        "qtd_faltas_terapeutas",
        "sessoes_perdidas_pacientes",
        "sessoes_perdidas_terapeutas",
        "receita_perdida_total"
    ])

    carregar_tabela_bigquery(
        df,
        "clinica-500413.gold.kpi_faltas_snapshot"
    )

    print("Gold faltas carregado no BigQuery")

    # =========================
    # FINAL AUDIT
    # =========================
    data_fim = datetime.now()
    tempo_execucao = (data_fim - data_inicio).total_seconds()

    cursor.execute("""
        UPDATE audit.etl_run_log
        SET
            status = %s,
            data_fim = %s,
            tempo_execucao_seg = %s,
            linhas_inseridas = %s,
            linhas_rejeitadas = %s
        WHERE id = %s
    """, (
        "SUCCESS",
        data_fim,
        tempo_execucao,
        linhas_inseridas,
        0,
        log_id
    ))

    conn.commit()

    print(f"Gold faltas finalizado: {linhas_inseridas} linhas")

except Exception as e:

    conn.rollback()

    data_fim = datetime.now()
    tempo_execucao = (data_fim - data_inicio).total_seconds()

    try:
        cursor.execute("""
            UPDATE audit.etl_run_log
            SET
                status = %s,
                data_fim = %s,
                tempo_execucao_seg = %s,
                mensagem_erro = %s
            WHERE id = %s
        """, (
            "ERROR",
            data_fim,
            tempo_execucao,
            str(e),
            log_id
        ))
        conn.commit()

    except:
        pass

    print(f"Erro GOLD faltas: {e}")

finally:
    cursor.close()
    conn.close()