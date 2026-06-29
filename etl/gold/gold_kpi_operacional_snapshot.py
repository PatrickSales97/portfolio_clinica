import getpass
from datetime import datetime

import pandas as pd  # type: ignore

from etl.utils.db_connection import get_connection
from etl.gcp.upload_bigquery import carregar_tabela_bigquery


conn = get_connection()
cursor = conn.cursor()

processo = "gold_kpi_operacional_snapshot"
tabela = "gold.kpi_operacional_snapshot"

data_inicio = datetime.now()
linhas_inseridas = 0

try:

    cursor.execute("""
        INSERT INTO audit.etl_run_log (
            processo, tabela, status, data_inicio, usuario_execucao
        )
        VALUES (%s,%s,%s,%s,%s)
        RETURNING id
    """, (processo, tabela, "RUNNING", data_inicio, getpass.getuser()))

    log_id = cursor.fetchone()[0]
    conn.commit()

    print("Iniciando GOLD Operacional...")

    # =========================
    # POSTGRES
    # =========================
    cursor.execute("""
        INSERT INTO gold.kpi_operacional_snapshot (
            data_referencia,
            pacientes_ativos,
            profissionais_ativos,
            sessoes_realizadas,
            sessoes_perdidas_pacientes,
            sessoes_perdidas_terapeutas,
            total_sessoes_operacionais
        )
        SELECT
            a.data_atd AS data_referencia,
            COUNT(DISTINCT a.id_paciente) AS pacientes_ativos,
            COUNT(DISTINCT a.id_profissional) AS profissionais_ativos,
            COUNT(a.id_atendimento) AS sessoes_realizadas,
            COALESCE(SUM(fp.qtd),0) AS sessoes_perdidas_pacientes,
            COALESCE(SUM(ft.qtd),0) AS sessoes_perdidas_terapeutas,
            COUNT(a.id_atendimento) +
            COALESCE(SUM(fp.qtd),0) +
            COALESCE(SUM(ft.qtd),0) AS total_sessoes_operacionais

        FROM silver.atendimentos a

        LEFT JOIN (
            SELECT data_falta, COUNT(*) AS qtd
            FROM silver.faltas_pacientes
            GROUP BY data_falta
        ) fp ON a.data_atd = fp.data_falta

        LEFT JOIN (
            SELECT data_falta, COUNT(*) AS qtd
            FROM silver.faltas_terapeutas
            GROUP BY data_falta
        ) ft ON a.data_atd = ft.data_falta

        GROUP BY a.data_atd

        ON CONFLICT (data_referencia)
        DO UPDATE SET
            pacientes_ativos = EXCLUDED.pacientes_ativos,
            profissionais_ativos = EXCLUDED.profissionais_ativos,
            sessoes_realizadas = EXCLUDED.sessoes_realizadas,
            sessoes_perdidas_pacientes = EXCLUDED.sessoes_perdidas_pacientes,
            sessoes_perdidas_terapeutas = EXCLUDED.sessoes_perdidas_terapeutas,
            total_sessoes_operacionais = EXCLUDED.total_sessoes_operacionais
    """)

    linhas_inseridas = cursor.rowcount
    conn.commit()

    # =========================
    # BIGQUERY
    # =========================
    cursor.execute("""
        SELECT *
        FROM gold.kpi_operacional_snapshot
    """)

    df = pd.DataFrame(cursor.fetchall(), columns=[
        "id",
        "data_referencia",
        "pacientes_ativos",
        "profissionais_ativos",
        "sessoes_realizadas",
        "sessoes_perdidas_pacientes",
        "sessoes_perdidas_terapeutas",
        "total_sessoes_operacionais",
        "data_carga"
    ])

    df = df.drop(columns=["id", "data_carga"])

    carregar_tabela_bigquery(df, "clinica-500413.gold.kpi_operacional_snapshot")

    print("Operacional OK")

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

except Exception as e:
    conn.rollback()
    print(f"Erro operacional: {e}")

finally:
    cursor.close()
    conn.close()