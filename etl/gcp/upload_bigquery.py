import pandas as pd # type: ignore
from google.cloud import bigquery

def carregar_tabela_bigquery(df, table_id, project_id="clinica-500413"):

    client = bigquery.Client(project=project_id)

    df = df.copy()

    # =========================
    # FORÇA datetime Python puro
    # =========================
    for col in ["data_pgto", "data_carga"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.to_pydatetime()

    # =========================
    # remove NaN
    # =========================
    df = df.where(pd.notnull(df), None)

    # =========================
    # SEM schema manual
    # SEM autodetect TRUE (evita inferência errada)
    # =========================
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=False
    )

    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config
    )

    job.result()

    print(f"BigQuery carregado: {table_id}")