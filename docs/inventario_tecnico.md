# Inventário Técnico

## Linguagens

* Python 3.12
* SQL

---

## Banco de Dados

### PostgreSQL

Schemas:

* audit
* bronze
* silver
* gold

---

### BigQuery

Projeto:

```text
clinica-500413
```

Datasets:

* audit
* bronze
* silver
* gold

---

## Bibliotecas Python

Principais:

```text
pandas
psycopg2
openpyxl
google-cloud-bigquery
pyarrow
```

---

## Orquestração

Airflow

Componentes:

```text
dag_luma_pipeline.py
pipeline_master.py
quality_runner.py
run_bronze.py
run_silver.py
run_gold.py
```

---

## Infraestrutura

Docker Desktop
WSL2 Ubuntu
Google Cloud Platform
GitHub Privado