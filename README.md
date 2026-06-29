# 📊 Luma Data Platform — Migração e Modernização de BI

## 🎯 Visão do Projeto

A Luma Data Platform é uma iniciativa de modernização da arquitetura de dados da Clínica Luma, evoluindo de processos manuais baseados em planilhas para uma plataforma de dados estruturada em camadas (Medallion Architecture), com suporte a orquestração completa via Apache Airflow e integração com cloud analytics (BigQuery).

O objetivo é garantir:
- confiabilidade dos dados
- rastreabilidade ponta a ponta
- escalabilidade do pipeline
- automação de processos de ETL
- base sólida para analytics e futuras aplicações de Data Engineering

---

# 🧠 Arquitetura Atual (Híbrida e Orquestrada)

O sistema opera em arquitetura híbrida entre **PostgreSQL local** e **BigQuery (cloud)**, com orquestração centralizada via **Apache Airflow**.

## 🔹 Pipeline Operacional (PostgreSQL)

```text
Fontes operacionais (ABA+ / Agilos / Excel)
        ↓
Ingestão via Python ETL
        ↓
Bronze Layer (raw ingestion)
        ↓
Silver Layer (data cleansing & standardization)
        ↓
Gold Layer (business-ready datasets)
        ↓
PostgreSQL (Luma Database)
```

---

## ☁️ Pipeline Analítico (BigQuery)

```text
PostgreSQL (Gold Layer)
        ↓
ETL de carga controlado (WRITE_TRUNCATE)
        ↓
BigQuery (Gold Dataset)
        ↓
Power BI / Analytics Layer
```

---

# 🏗️ Arquitetura Medalhão

## 🟤 Bronze Layer (Raw Data)

Camada responsável pela ingestão fiel dos dados de origem.

**Características:**
- dados brutos (sem transformação)
- preservação do estado original
- suporte a reprocessamento completo
- rastreabilidade de origem

---

## ⚪ Silver Layer (Trusted Data)

Camada de padronização e confiabilidade.

**Características:**
- limpeza e normalização
- tratamento de tipos de dados
- padronização de chaves
- preparação analítica intermediária

---

## 🟡 Gold Layer (Business Layer)

Camada analítica orientada ao negócio.

**Características:**
- KPIs e métricas executivas
- snapshots de desempenho
- datasets consumidos por BI
- base para exportação ao BigQuery

---

## ☁️ BigQuery Layer (Analytics Cloud)

Camada final de consumo analítico em cloud.

**Características:**
- carga FULL REFRESH via `WRITE_TRUNCATE`
- sem uso de UPDATE/DELETE manual
- reprocessamento completo por execução
- integração com Power BI e futuras aplicações

---

# ⚙️ Estratégia de Carga de Dados

## PostgreSQL

- Bronze: ingestão bruta (reprocessável)
- Silver: transformação determinística
- Gold: snapshots analíticos

## BigQuery

- estratégia FULL REFRESH
- controle via `WRITE_TRUNCATE`
- ausência de upsert manual
- fonte única: Gold layer

---

# 🔄 Orquestração (Apache Airflow)

O pipeline é totalmente orquestrado via Apache Airflow, com execução modular por camada.

Além disso, foram realizados testes manuais independentes (scripts Python isolados) com o objetivo de validação e segurança antes da consolidação do fluxo automatizado.

## DAGs principais

- Bronze ingestion DAG
- Silver transformation DAG
- Gold aggregation DAG
- Pipeline master (orquestração geral)

## Execução manual (debug/testes)

```bash
python -m etl.orchestrator.pipeline_master
```

## Execução via Airflow

Execução automatizada via DAGs agendadas no Airflow Scheduler e Workers.

---

# 📊 Observabilidade e Auditoria

O sistema possui rastreabilidade completa de execução.

## Recursos implementados:
- logs de execução por ETL
- controle de linhas inseridas e rejeitadas
- tempo de execução por processo
- auditoria de pipelines

## Schema de auditoria:

```sql
audit.etl_run_log
```

---

# 🐳 Infraestrutura

Ambiente containerizado com:

- PostgreSQL (Docker)
- Airflow (orquestração)
- ETL Python runtime (Docker)
- Docker Compose
- volumes persistentes
- suporte a execução local padronizada

---

# 🛠️ Tecnologias

- Python (ETL core)
- Apache Airflow (orquestração)
- PostgreSQL (operational + staging)
- BigQuery (cloud analytics layer)
- Docker / Docker Compose
- pandas
- psycopg2
- Google Cloud BigQuery Client
- Power BI
- Git / GitHub

---

# 📁 Estrutura do Projeto

```text
etl/
 ├── bronze/         # ingestion layer
 ├── silver/         # transformation layer
 ├── gold/           # analytics layer
 ├── orchestrator/   # pipeline control
 └── utils/          # shared utilities

sql/
 ├── bronze/
 ├── silver/
 ├── gold/
 └── audit/

data/
docker/
logs/
powerbi/
docs/
```

---

# 🚀 Roadmap Técnico

## Concluído
- [x] Arquitetura Medallion (Bronze/Silver/Gold)
- [x] Pipeline ETL funcional em PostgreSQL
- [x] Camada Gold operacional
- [x] Integração com BigQuery
- [x] Orquestração via Apache Airflow
- [x] Estratégia de carga FULL REFRESH

## Em evolução
- [ ] Data Quality automatizado (tests e validações)
- [ ] Incremental loads (MERGE strategy no BigQuery)
- [ ] Monitoramento centralizado
- [ ] Observabilidade avançada
- [ ] Otimização de performance de DAGs

---

# 📌 Status Atual do Projeto

O sistema encontra-se em estágio funcional avançado, com arquitetura Medallion totalmente implementada e orquestrada via Apache Airflow.

O pipeline suporta execução automatizada por DAGs, com validações manuais realizadas durante a fase de estabilização e testes.

A camada analítica está integrada ao BigQuery com estratégia de carga FULL REFRESH, garantindo consistência e reprocessamento controlado entre ambientes.

---

# 💡 Nota de Arquitetura

Este projeto adota uma abordagem moderna de engenharia de dados híbrida e orquestrada:

- PostgreSQL como camada operacional e staging
- BigQuery como camada analítica escalável
- Airflow como orquestrador central do pipeline
- ETL em Python com controle modular por camada
- Estratégia de carga baseada em reprocessamento determinístico (FULL REFRESH)