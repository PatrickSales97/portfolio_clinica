from google.cloud import bigquery

# cliente (usa login do gcloud automaticamente - ADC)
client = bigquery.Client(project="luma-496811")

table_id = "luma-496811.bronze.teste_conexao"

# dados de teste
rows = [
    {
        "id": 10,
        "nome": "adc_step1",
        "data": "2026-01-01"
    }
]

# =========================
# CARGA VIA LOAD JOB (NÃO STREAMING)
# =========================
job_config = bigquery.LoadJobConfig(
    write_disposition="WRITE_APPEND"  # ou WRITE_TRUNCATE se quiser sobrescrever
)

job = client.load_table_from_json(
    rows,
    table_id,
    job_config=job_config
)

job.result()  # espera finalizar

print("INSERT OK via LOAD JOB")

# =========================
# VALIDAÇÃO
# =========================
query = f"""
SELECT *
FROM `{table_id}`
ORDER BY id DESC
LIMIT 5
"""

query_job = client.query(query)

for row in query_job:
    print(row)