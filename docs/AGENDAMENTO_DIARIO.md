# ⏰ Agendamento Diário da DAG Airflow

## 🎯 O que foi feito

Atualizei a DAG `luma_pipeline` para rodar **automaticamente todos os dias às 02:00 AM (2h da manhã)**.

### Antes:
```python
schedule=None  # ❌ Sem agendamento (manual only)
```

### Depois:
```python
schedule="0 2 * * *"  # ✅ Todos os dias às 02:00 AM
```

---

## 📅 Opções de Agendamento

### ⏰ Predefinidas (Recomendado - mais legível)
```python
schedule="@daily"           # Diariamente à meia-noite
schedule="@hourly"          # A cada hora
schedule="@weekly"          # Toda segunda-feira à meia-noite
schedule="@monthly"         # 1º de cada mês à meia-noite
schedule="@yearly"          # 1º de janeiro à meia-noite
schedule=None               # Manual (sem agendamento)
```

### 🔧 Expressões CRON (Mais flexível)
```python
# Formato: "minuto hora dia_mes mes dia_semana"
schedule="0 2 * * *"        # Diariamente às 02:00 (nosso caso)
schedule="0 2 * * 1"        # Segunda-feira às 02:00
schedule="0 2,14 * * *"     # Às 02:00 e às 14:00 (2 vezes/dia)
schedule="*/30 * * * *"     # A cada 30 minutos
schedule="0 0 * * *"        # Meia-noite (padrão @daily)
schedule="0 */4 * * *"      # A cada 4 horas
```

### 🎨 Exemplos Úteis
```python
# Rodar de madrugada (quando sistema está menos ocupado)
schedule="0 3 * * *"        # 03:00 AM todos os dias

# Rodar em horário comercial
schedule="0 9 * * 1-5"      # 09:00 AM segunda a sexta

# Rodar 2x ao dia
schedule="0 6,18 * * *"     # 06:00 AM e 06:00 PM

# Rodar no 1º dia do mês
schedule="0 2 1 * *"        # 02:00 AM no 1º de cada mês

# Executar cada 6 horas
schedule="0 */6 * * *"      # 00:00, 06:00, 12:00, 18:00
```

---

## ✅ Configurações Adicionadas

Também adicionei melhorias no agendamento:

### 1. **default_args** (Padrões globais)
```python
default_args = {
    'owner': 'luma_etl',           # Dono da DAG
    'retries': 2,                   # Tenta 2x se falhar
    'retry_delay': timedelta(minutes=5),  # Espera 5min entre tentativas
    'email_on_failure': False,      # Não envia email em erro
    'email_on_retry': False,        # Não envia email em retry
}
```

### 2. **Tratamento de Erros**
- ✅ Se falhar, tenta novamente 2 vezes
- ✅ Aguarda 5 minutos entre tentativas
- ✅ Sem travamentos

---

## 🚀 Como Funciona

### Timeline Diária
```
02:00 AM ─────► DAG inicia
02:01 AM ─────► ETL Bronze começa
02:01 AM ─────► ETL Silver
02:02 AM ─────► ETL Gold
02:02 AM ─────► Quality Validation
02:03 AM ◄───── DAG finaliza (✅ sucesso)

Se falhar:
02:03 AM ─────► Retry 1 (aguarda 5 min)
02:08 AM ─────► Executa novamente
```

---

## 📊 Monitorar Agendamento

### 1. **Interface Web do Airflow**
```
http://localhost:8080
```
- Acesse a DAG `luma_pipeline`
- Você verá as próximas execuções agendadas
- Histórico de execuções anteriores

### 2. **Via CLI**
```bash
# Ver próximas execuções agendadas
docker exec -it airflow_webserver airflow dags list-runs -d luma_pipeline

# Ver status atual
docker exec -it airflow_webserver airflow dags list | grep luma

# Ver logs da última execução
docker logs airflow_scheduler | grep luma_pipeline
```

### 3. **Logs em Tempo Real**
```bash
docker logs -f airflow_scheduler | grep -i "luma"
```

---

## 🔧 Como Mudar o Horário

Se quiser alterar para **3 da manhã**:

```python
schedule="0 3 * * *"  # 03:00 AM
```

Se quiser **18:00 (6 PM)**:

```python
schedule="0 18 * * *"  # 18:00 (6 PM)
```

Se quiser **duas vezes ao dia** (02:00 e 14:00):

```python
schedule="0 2,14 * * *"
```

---

## ⚙️ Scheduler do Airflow

### O que faz:
1. ✅ Monitora as DAGs constantemente
2. ✅ Verifica se alguma deve ser executada
3. ✅ Dispara DAGs no horário agendado
4. ✅ Registra todos os logs
5. ✅ Trata falhas e retries

### Status
```bash
# Ver se scheduler está rodando
docker exec -it airflow_scheduler ps aux | grep scheduler

# Deve aparecer assim:
airflow scheduler (running for X hours)
```

---

## 📌 Próximas Execuções Agendadas

Com a configuração atual (`0 2 * * *`), a DAG rodará:

- ✅ Hoje (2026-06-03) às 02:00 AM
- ✅ Amanhã (2026-06-04) às 02:00 AM
- ✅ E assim sucessivamente, todo dia...

---

## 🎯 Resumo

| Aspecto | Antes | Depois |
|--------|-------|--------|
| Agendamento | Manual | ✅ Automático diário |
| Horário | N/A | ✅ 02:00 AM |
| Retries | Nenhum | ✅ 2 tentativas |
| Delay | N/A | ✅ 5 minutos |
| Status | ❌ Manual | ✅ 100% Automático |

---

## 🚀 Próximos Passos

1. ✅ DAG agora roda automaticamente
2. ⏳ Monitore a primeira execução automática
3. ⏳ Ajuste horário conforme necessário
4. ⏳ Adicione alertas de erro (email, Slack, etc)

---

**Arquivo atualizado:** `airflow/dags/dag_luma_pipeline.py`  
**Agendamento ativo:** ✅ 02:00 AM todos os dias

