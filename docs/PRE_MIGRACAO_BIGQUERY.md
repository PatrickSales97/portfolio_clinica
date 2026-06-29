# 🚀 Plano de Migração - PostgreSQL Local → Google Cloud BigQuery

## 📋 Antes de Começar - O Que Você Precisa Fazer

### Pré-requisitos no Google Cloud

Para que eu possa começar a codificar, você precisa ter:

#### 1. **Conta Google Cloud ativa**
- ✅ Já tem uma conta GCP?
- ✅ Projeto criado no GCP?
- ❓ Qual é o ID do projeto? (ex: `projeto-luma-123`)

#### 2. **BigQuery ativado**
```bash
# No Console do GCP:
# APIs & Services > Library > BigQuery API > Enable
```

#### 3. **Arquivo de Credenciais (Service Account)**
```bash
# No Console do GCP:
1. IAM & Admin > Service Accounts
2. Create Service Account
3. Dar permissão: "BigQuery Admin" ou "BigQuery Data Editor"
4. Baixar como JSON (arquivo .json)
```

**Esse arquivo JSON é crítico!** Você vai precisar dele.

#### 4. **BigQuery Dataset criado**
```bash
# No Console do GCP ou via CLI:
# Criar um dataset chamado "luma" (ou outro nome que preferir)

# Via CLI:
bq mk --dataset luma

# Via Console:
# BigQuery > Datasets > Create Dataset > Nome: luma
```

#### 5. **Estrutura de Tabelas no BigQuery**
Preciso saber:
- ✅ Quer manter a mesma estrutura? (bronze → silver → gold)
- ✅ Quer compactações? (remover staging tables?)
- ✅ Particionamento por data?
- ✅ Clustering por alguma coluna?

---

## 🎯 O Que Você Deve Fazer AGORA

### ✅ Checklist Pre-Implementação

```
☐ 1. Conta Google Cloud criada
☐ 2. Projeto GCP criado (anote o ID)
☐ 3. BigQuery API ativada
☐ 4. Service Account criado
☐ 5. Credenciais baixadas (arquivo .json)
☐ 6. Dataset "luma" criado no BigQuery
☐ 7. Definiu estrutura de tabelas (bronze/silver/gold ou outra?)
☐ 8. Decidiu sobre particionamento/clustering
```

---

## 📦 Arquivos que Você Precisa Me Enviar

1. **Arquivo de credenciais JSON**
   - Caminho: `~/.config/gcloud/service-account-luma.json`
   - Ou qualquer lugar seguro do seu projeto

2. **Informações do GCP:**
   - Project ID
   - Dataset name
   - Região (us-central1, us-east1, etc)

---

## 🔄 Fluxo de Migração (O que farei depois)

```
┌─────────────────────────────────────────────────────┐
│  Seu PostgreSQL Local/Docker                         │
│  (bronze, silver, gold tables)                       │
└────────────────┬────────────────────────────────────┘
                 │
                 │ ETL Adapter
                 ▼
┌─────────────────────────────────────────────────────┐
│  Google Cloud BigQuery                               │
│  (luma.bronze.*, luma.silver.*, luma.gold.*)        │
│                                                      │
│  + Power BI connects directly to BigQuery           │
│  + Real-time dashboards                            │
│  + Scalable analytics                              │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ O Que Vou Criar

Após você preparar tudo, vou fazer:

### 1. **Módulo de Conexão com BigQuery**
```python
etl/utils/bigquery_connection.py
```

### 2. **Script de Migração Inicial (full load)**
```python
etl/orchestrator/bigquery_migrator.py
```

### 3. **DAG de Replicação Contínua**
```python
airflow/dags/dag_bigquery_sync.py
```

### 4. **Transformações para BigQuery**
```python
etl/bigquery/
  ├── bronze_to_bigquery.py
  ├── silver_to_bigquery.py
  └── gold_to_bigquery.py
```

### 5. **Configurações e Documentação**
- `docs/MIGRACAO_BIGQUERY.md`
- `.env.bigquery`
- Credentials management

---

## 💰 Considerações de Custo

**Google Cloud BigQuery tem modelo de pagamento:**
- ✅ Primeiro 1 TB/mês = GRÁTIS
- 💸 Acima disso = ~$6.25 por TB

**Seu volume atual:** ~49K registros = negligenciável
- Está bem dentro do free tier

**Storage:** ~50 MB/mês = ~$0.02/mês (praticamente grátis)

---

## 📱 Opções de Autenticação

Você pode usar:

### Option 1: Service Account (Recomendado - Produção)
```python
from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    '/path/to/service-account.json'
)
client = bigquery.Client(credentials=credentials)
```

### Option 2: Application Default Credentials
```bash
gcloud auth application-default login
# Usa suas credenciais pessoais do gcloud
```

### Option 3: API Key (Simples - Dev)
```python
# Menos seguro, só para testes
```

---

## ⏳ Timeline de Implementação

```
Fase 1: Preparação (Você faz - 30-60 min)
├─ Criar conta GCP
├─ Criar projeto
├─ Ativar BigQuery
├─ Criar Service Account
└─ Baixar JSON

Fase 2: Implementação (Eu faço - 2-4 horas)
├─ Criar módulos de conexão
├─ Fazer migração inicial
├─ Testar replicação
└─ Integrar com Airflow

Fase 3: Validação (Você valida - 30 min)
├─ Verificar dados no BigQuery
├─ Testar Power BI connection
└─ Confirmar sincronização

Fase 4: Productização (Eu faço - 1-2 horas)
├─ Otimizar queries
├─ Configurar particionamento
├─ Setup de backups
└─ Documentação final
```

---

## 🎯 Decisões Necessárias

Responda antes de eu começar:

1. **Estrutura de Tabelas:**
   - Manter bronze/silver/gold? (SIM/NÃO)
   - Renomear conforme GCP standards? (Ex: raw, staging, analytics)

2. **Particionamento:**
   - Por data (data_carga)? (SIM/NÃO)
   - Por outra coluna? (QUAL)

3. **Clustering:**
   - Por paciente_id? (SIM/NÃO)
   - Por profissional_id? (SIM/NÃO)
   - Por outra? (QUAL)

4. **Replicação:**
   - Toda vez que roda DAG? (FULL SYNC)
   - Só novos registros? (INCREMENTAL)
   - Ambos? (HYBRID)

5. **Power BI:**
   - Conectar direto ao BigQuery?
   - Ou criar views específicas?

---

## 🚀 Próximos Passos

### ✅ Você faz agora:
1. Criar conta GCP (se não tiver)
2. Criar projeto
3. Habilitar BigQuery
4. Criar Service Account
5. Baixar JSON
6. Criar dataset "luma"

### ⏳ Depois:
Me avisa quando tudo está pronto!
- Compartilhe o ID do projeto
- Informe o nome do dataset
- Responda as decisões acima

### 🔥 Aí sim:
Eu codifico toda a integração!

---

**Precisa de ajuda com os passos do Google Cloud?**
Posso criar um guia passo a passo visual também!

