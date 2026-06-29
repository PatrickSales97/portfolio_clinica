# 🐳 Guia de Validação - Banco Docker + DAG Airflow

## 📋 Passos para Validar e Testar

### **Passo 1: Verificar se Docker está rodando**

```powershell
# Listar containers
docker ps

# Resultado esperado deve mostrar:
# - postgres_luma (banco de dados)
# - airflow_webserver (interface Airflow)
# - airflow_scheduler (orquestrador)
```

### **Passo 2: Acessar o PostgreSQL do Docker**

#### **Opção A: Via psql (mais direto)**

```powershell
# Conectar ao banco PostgreSQL dentro do Docker
docker exec -it postgres_luma psql -U postgres -d Luma

# Comandos SQL úteis dentro do psql:
\dt                                    # Listar todas as tabelas
\d schema_name.table_name              # Ver estrutura da tabela
SELECT * FROM information_schema.schemata;  # Listar schemas
\q                                     # Sair

# Exemplo completo:
docker exec -it postgres_luma psql -U postgres -d Luma -c "SELECT COUNT(*) FROM bronze.atendimentos_raw;"
```

#### **Opção B: Via DBeaver/TablePlus (GUI)**
1. **Host:** `localhost`
2. **Port:** `5432`
3. **Database:** `Luma`
4. **User:** `postgres`
5. **Password:** `Luma@4862`

---

## ✅ Checklist de Validação PRÉ-DAG

Execute esses comandos ANTES de rodar a DAG para ter uma baseline:

```powershell
# 1️⃣ Verificar tabelas de bronze
docker exec -it postgres_luma psql -U postgres -d Luma -c "
SELECT 'bronze.atendimentos_raw' as tabela, COUNT(*) as registros FROM bronze.atendimentos_raw
UNION ALL
SELECT 'bronze.faltas_pacientes', COUNT(*) FROM bronze.faltas_pacientes
UNION ALL
SELECT 'bronze.faltas_terapeutas', COUNT(*) FROM bronze.faltas_terapeutas;
"

# 2️⃣ Verificar tabelas de dimensão
docker exec -it postgres_luma psql -U postgres -d Luma -c "
SELECT 'bronze.d_pacientes' as tabela, COUNT(*) as registros FROM bronze.d_pacientes
UNION ALL
SELECT 'bronze.d_profissionais', COUNT(*) FROM bronze.d_profissionais
UNION ALL
SELECT 'bronze.d_convenios', COUNT(*) FROM bronze.d_convenios;
"

# 3️⃣ Verificar silver (camada intermediária)
docker exec -it postgres_luma psql -U postgres -d Luma -c "
SELECT 'silver.atendimentos' as tabela, COUNT(*) as registros FROM silver.atendimentos
UNION ALL
SELECT 'silver.faltas_pacientes', COUNT(*) FROM silver.faltas_pacientes
UNION ALL
SELECT 'silver.faltas_terapeutas', COUNT(*) FROM silver.faltas_terapeutas;
"

# 4️⃣ Verificar gold (camada final)
docker exec -it postgres_luma psql -U postgres -d Luma -c "
SELECT 'gold.kpi_operacional' as tabela, COUNT(*) as registros FROM gold.kpi_operacional
UNION ALL
SELECT 'gold.kpi_faturamento', COUNT(*) FROM gold.kpi_faturamento
UNION ALL
SELECT 'gold.kpi_faltas', COUNT(*) FROM gold.kpi_faltas;
"

# 5️⃣ Ver logs da última execução
docker exec -it postgres_luma psql -U postgres -d Luma -c "
SELECT processo, status, data_inicio, COALESCE(data_fim, 'Rodando...') FROM audit.etl_run_log 
ORDER BY data_inicio DESC LIMIT 5;
"
```

---

## 🚀 Executar a DAG Manualmente

### **Opção 1: Via CLI Airflow (recomendado)**

```powershell
# Testar a DAG (valida sintaxe sem executar)
docker exec -it airflow_webserver airflow dags test luma_pipeline

# Rodar a DAG uma única vez (para este teste)
docker exec -it airflow_webserver airflow dags test luma_pipeline 2026-06-02

# Ver status em tempo real
docker logs -f airflow_scheduler
docker logs -f airflow_webserver
```

### **Opção 2: Via Interface Web (mais visual)**

1. Abra: **http://localhost:8080**
2. Login padrão Airflow (se necessário)
3. Procure por `luma_pipeline`
4. Clique em **▶ Trigger DAG**
5. Monitore em tempo real na interface

---

## 📊 Validação PÓS-DAG

Após executar, rode novamente os comandos acima e compare:

```powershell
# Comando equivalente para BANCO LOCAL também
# (para comparar se dados sincronizaram)

# LOCAL (mesmo computador, porta local)
psql -U postgres -d Luma -h localhost -p 5432 -c "SELECT COUNT(*) FROM bronze.atendimentos_raw;"

# DOCKER (via container)
docker exec -it postgres_luma psql -U postgres -d Luma -c "SELECT COUNT(*) FROM bronze.atendimentos_raw;"

# Os dois devem retornar o MESMO número!
```

---

## 🔍 Troubleshooting

### **"Connection refused"**
```powershell
# Verificar se containers estão rodando
docker ps

# Se não estão, iniciar:
cd docker
docker-compose up -d
```

### **"Role does not exist"**
```powershell
# O container pode estar iniciando. Aguarde 10-15 segundos e tente novamente
Start-Sleep -Seconds 15
docker exec -it postgres_luma psql -U postgres -d Luma -c "SELECT 1;"
```

### **DAG não aparece em "luma_pipeline"**
```powershell
# Recarregar DAGs no Airflow
docker exec -it airflow_webserver airflow dags list

# Se ainda não aparecer, verificar logs
docker logs airflow_scheduler | Select-String "luma_pipeline"
```

### **Dados não sincronizaram entre LOCAL e DOCKER**
```powershell
# 1. Verificar se USE_DUAL_CONNECTION está ativo
docker exec -it airflow_scheduler env | Select-String "USE_DUAL_CONNECTION"

# 2. Ver logs detalhados da execução
docker logs airflow_scheduler | tail -100
```

---

## 📝 Script Rápido de Comparação

Salve como `compare_banks.ps1`:

```powershell
# Compara ambos os bancos
$query = "SELECT COUNT(*) FROM bronze.atendimentos_raw;"

Write-Host "=== BANCO LOCAL ===" -ForegroundColor Green
psql -U postgres -d Luma -h localhost -p 5432 -c $query

Write-Host "`n=== BANCO DOCKER ===" -ForegroundColor Blue
docker exec -it postgres_luma psql -U postgres -d Luma -c $query

Write-Host "`n✅ Se os números forem iguais, sincronização funcionou!" -ForegroundColor Cyan
```

Execute:
```powershell
.\compare_banks.ps1
```

---

## 🎯 Flow Recomendado Hoje

1. ✅ Verifique se containers estão rodando
2. ✅ Execute o checklist PRÉ-DAG
3. ✅ Rode a DAG manualmente
4. ✅ Monitore logs em tempo real
5. ✅ Execute o checklist PÓS-DAG
6. ✅ Compare LOCAL vs DOCKER

Se todos os números baterem = **infra validada** ✨

---

**Dúvidas?** Me chama!
