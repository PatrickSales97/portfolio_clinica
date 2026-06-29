# Arquitetura Atual - Projeto Migração BI Luma

## Objetivo

Migrar a solução atual baseada em PostgreSQL para uma arquitetura moderna de dados utilizando Google Cloud Platform (BigQuery), mantendo compatibilidade com os dashboards existentes durante o processo de transição.

---

## Arquitetura Atual

### Fonte de Dados

Arquivos Excel:

* f_atendimento.xlsm
* f_faltas_pac.xlsx
* f_faltas_ter.xlsx
* d_profissionais.xlsx
* d_pacientes.xlsx
* d_convenios.xlsx

Localização:

```text
data/raw/
```

---

## Camada Bronze

Objetivo:

Armazenar os dados brutos com mínima transformação.

Tabelas:

```text
bronze.atendimentos_raw
bronze.faltas_pacientes_raw
bronze.faltas_terapeutas_raw
bronze.profissionais_raw
bronze.pacientes_raw
bronze.convenios_raw
```

Características:

* UPSERT por chave de negócio
* Auditoria automática
* Carga simultânea PostgreSQL + BigQuery

Dataset BigQuery:

```text
bronze
```

---

## Camada Silver

Objetivo:

Padronização, tipagem e aplicação de regras de negócio.

Tabelas:

```text
silver.atendimentos
silver.faltas_pacientes
silver.faltas_terapeutas
```

Características:

* Conversão de tipos
* Cálculo de receita bruta
* Cálculo de receita perdida
* Relacionamento por IDs
* UPSERT incremental

Dataset BigQuery:

```text
silver
```

---

## Camada Gold

Objetivo:

Disponibilizar indicadores analíticos para consumo do BI.

Tabelas:

```text
gold.kpi_faturamento_snapshot
gold.kpi_faltas_snapshot
gold.kpi_operacional_snapshot
```

Características:

* Agregações
* KPIs de negócio
* Consumo para Power BI

Dataset BigQuery:

```text
gold
```

---

## Auditoria

Tabela:

```text
audit.etl_run_log
```

Registrado em:

* PostgreSQL
* BigQuery

Campos:

* processo
* tabela
* status
* data_inicio
* data_fim
* tempo_execucao_seg
* linhas_inseridas
* linhas_rejeitadas
* mensagem_erro
* usuario_execucao

---

## Orquestração

Airflow executando em Docker.

Estrutura:

```text
docker/
airflow/
etl/
```

Containers:

* airflow-webserver
* airflow-scheduler
* postgres

---

## Google Cloud Platform

Projeto:

```text
clinica-500413
```

Datasets:

```text
audit
bronze
silver
gold
```

Todas as cargas utilizam:

```python
WRITE_TRUNCATE
```

garantindo sincronização completa entre PostgreSQL e BigQuery.