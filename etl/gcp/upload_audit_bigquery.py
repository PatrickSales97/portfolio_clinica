import pandas as pd # type: ignore

from google.cloud import bigquery

from etl.utils.db_connection import get_connection


def atualizar_audit_bigquery():

    conn = get_connection()

    query = """
    SELECT
        id,
        processo,
        tabela,
        status,
        data_inicio,
        data_fim,
        tempo_execucao_seg,
        linhas_inseridas,
        linhas_rejeitadas,
        mensagem_erro,
        usuario_execucao
    FROM audit.etl_run_log
    """

    df = pd.read_sql(query, conn)

    conn.close()

    client = bigquery.Client(
        project="clinica-500413"
    )

    table_id = (
        "clinica-500413.audit.etl_run_log"
    )

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE"
    )

    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config
    )

    job.result()

    print(
        "Audit sincronizada com BigQuery"
    )