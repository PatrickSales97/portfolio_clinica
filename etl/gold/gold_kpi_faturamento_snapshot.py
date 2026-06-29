import getpass
from datetime import datetime

import pandas as pd  # type: ignore

from etl.utils.db_connection import get_connection
from etl.gcp.upload_bigquery import carregar_tabela_bigquery


conn = get_connection()
cursor = conn.cursor()

processo = "gold_kpi_faturamento_snapshot"
tabela = "gold.kpi_faturamento_snapshot"

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

    print("Iniciando GOLD Faturamento...")

    # =========================
    # POSTGRES LOAD
    # =========================
    cursor.execute("""
        INSERT INTO gold.kpi_faturamento_snapshot (
            data_referencia,
            receita_bruta,
            receita_glosada,
            receita_liquida,
            qtd_sessoes,
            ticket_medio
        )
        SELECT
            data_atd AS data_referencia,
            SUM(receita_bruta) AS receita_bruta,
            0 AS receita_glosada,
            SUM(receita_bruta) AS receita_liquida,
            SUM(qtd_sessao) AS qtd_sessoes,
            CASE 
                WHEN SUM(qtd_sessao) = 0 THEN 0
                ELSE SUM(receita_bruta) / SUM(qtd_sessao)
            END AS ticket_medio
        FROM silver.atendimentos
        GROUP BY data_atd

        ON CONFLICT (data_referencia)
        DO UPDATE SET
            receita_bruta = EXCLUDED.receita_bruta,
            receita_glosada = EXCLUDED.receita_glosada,
            receita_liquida = EXCLUDED.receita_liquida,
            qtd_sessoes = EXCLUDED.qtd_sessoes,
            ticket_medio = EXCLUDED.ticket_medio
    """)

    linhas_inseridas = cursor.rowcount
    conn.commit()

    # =========================
    # BIGQUERY LOAD
    # =========================
    cursor.execute("""
        SELECT
            data_referencia,
            receita_bruta,
            receita_glosada,
            receita_liquida,
            qtd_sessoes,
            ticket_medio
        FROM gold.kpi_faturamento_snapshot
    """)

    df = pd.DataFrame(cursor.fetchall(), columns=[
        "data_referencia",
        "receita_bruta",
        "receita_glosada",
        "receita_liquida",
        "qtd_sessoes",
        "ticket_medio"
    ])

    carregar_tabela_bigquery(df, "clinica-500413.gold.kpi_faturamento_snapshot")

    # =========================
    # AUDIT SUCCESS
    # =========================
    data_fim = datetime.now()
    tempo_execucao = (data_fim - data_inicio).total_seconds()

    cursor.execute("""
        UPDATE audit.etl_run_log
        SET status=%s,
            data_fim=%s,
            tempo_execucao_seg=%s,
            linhas_inseridas=%s,
            linhas_rejeitadas=%s
        WHERE id=%s
    """, ("SUCCESS", data_fim, tempo_execucao, linhas_inseridas, 0, log_id))

    conn.commit()

    print(f"Faturamento OK: {linhas_inseridas} linhas")

except Exception as e:
    conn.rollback()
    print(f"Erro faturamento: {e}")

finally:
    cursor.close()
    conn.close()