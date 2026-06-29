# 🏥 Projeto Clínico — Pipeline de Dados & Inteligência de Negócio

Este projeto simula um ecossistema completo de dados para uma clínica, com foco em **engenharia de dados, automação de pipelines e geração de insights estratégicos** para tomada de decisão.

Os dados utilizados são **fictícios, gerados para fins de portfólio (via Gemini)**.

---

# 🚀 Objetivo do Projeto

Construir uma solução completa de dados capaz de:

- Integrar diferentes fontes de dados (Excel, CSV, XLSM)
- Automatizar processos de ETL
- Organizar dados em camadas estruturadas (Bronze, Silver, Gold)
- Disponibilizar dados em um Data Warehouse escalável (BigQuery)
- Criar dashboards analíticos para suporte à decisão (Looker Studio)

---

# 🧠 Problema de Negócio Simulado

Clínicas enfrentam desafios como:

- Falta de visibilidade sobre rentabilidade por convênio e paciente
- Alto impacto financeiro causado por faltas de pacientes e profissionais
- Dados espalhados em planilhas sem padronização
- Dificuldade em medir eficiência operacional e financeira

---

# 💡 Solução Proposta

Foi desenvolvido um pipeline completo de dados com foco em:

- Automação de ingestão e transformação de dados
- Padronização e limpeza em múltiplas camadas
- Geração de indicadores estratégicos (KPIs)
- Visualização de dados para suporte à decisão

---

# 🏗️ Arquitetura do Projeto

## 🔹 Fontes de Dados
- Arquivos Excel (.xlsx, .xlsm)
- Arquivos CSV

## 🔹 Pipeline de Dados
- Python (ETL customizado)
- Apache Airflow (orquestração via Docker)

## 🔹 Data Warehouse
- Google BigQuery (camadas Bronze, Silver e Gold)

## 🔹 Visualização
- Looker Studio (Dashboard de Gestão Estratégica)

---

# 🧱 Arquitetura em Camadas (Medallion)

## 🥉 Bronze (Raw Data)
- Ingestão direta dos arquivos
- Sem transformações
- Dados brutos preservados

## 🥈 Silver (Tratamento)
- Limpeza e padronização
- Correção de tipos (datas, IDs, formatos)
- Normalização de colunas

## 🥇 Gold (Analytics)
- KPIs de negócio
- Views para análise estratégica
- Base para dashboards

---

# ⚙️ Orquestração

O pipeline é automatizado via **Apache Airflow (Docker)**:

- Execução agendada de DAGs
- Controle de dependências entre tarefas
- Monitoramento de execução
- Reprocessamento automático em caso de falhas

---

# 📦 Tecnologias Utilizadas

- Python (Pandas)
- Apache Airflow
- Docker
- Google BigQuery
- Looker Studio
- Google Cloud Platform (GCP)

---

# 📊 Dashboard Analítico

📌 Projeto: **Projeto Clínico - Dashboard de Gestão Estratégica**

## Visões disponíveis:

### 🧭 Executiva
- Visão geral da clínica
- KPIs de performance

### 📉 Faltas
- Análise de faltas de pacientes e profissionais
- Impacto financeiro
- Ranking de ocorrências

### ⚙️ Eficiência Operacional
- Produtividade por profissional
- Utilização de agenda
- Indicadores de performance

### 💰 Financeiro
- Rentabilidade por convênio
- Lucro e prejuízo estimado
- Perdas operacionais

---

# 📈 Insights Gerados

- Identificação de convênios menos rentáveis
- Profissionais com maior impacto em faltas
- Pacientes com maior taxa de ausência
- Estimativa de perdas financeiras por ineficiência operacional

---

# 🔄 Fluxo do Pipeline

1. Ingestão de arquivos (Excel/CSV)
2. Processamento Bronze (raw → BigQuery)
3. Transformação Silver (limpeza e padronização)
4. Criação de métricas Gold (KPIs)
5. Consumo no Looker Studio

---

# 🎯 Resultados Esperados

- Redução de perdas financeiras invisíveis
- Melhor tomada de decisão baseada em dados
- Visibilidade completa da operação da clínica
- Aumento de eficiência operacional

---

# 🧪 Observação

Este projeto é um **case de portfólio**, utilizando dados fictícios gerados para fins educacionais e demonstrativos.

---

# 👨‍💻 Autor

Projeto desenvolvido por **Patrick Almeida**  
Focado em Engenharia de Dados, BI e Cloud (GCP)

---

# 📌 Status

✔ Pipeline funcional  
✔ Orquestração com Airflow  
✔ ETL em Python  
✔ Data Warehouse no BigQuery  
✔ Dashboard no Looker Studio