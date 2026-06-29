from google.cloud import bigquery
import pandas as pd # type: ignore
from etl.utils.settings import BQ_PROJECT_ID

def load_to_bq(df, table_name, dataset_name, mode="replace"):
    # Cliente sem location (assume o padrão do projeto)
    client = bigquery.Client(project=BQ_PROJECT_ID)
    table_id = f"{BQ_PROJECT_ID}.{dataset_name}.{table_name}"
    
    # Tratamento para evitar erro de datetime vs int
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
            
    # Converte tudo para string para garantir compatibilidade total no upload
    df = df.astype(str)
    
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE" if mode == "replace" else "WRITE_APPEND"
    )
    
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    print(f"Sucesso: {table_id} carregada.")

def read_from_bq(dataset_name, table_name):
    client = bigquery.Client(project=BQ_PROJECT_ID)
    query = f"SELECT * FROM `{BQ_PROJECT_ID}.{dataset_name}.{table_name}`"
    return client.query(query).to_dataframe()