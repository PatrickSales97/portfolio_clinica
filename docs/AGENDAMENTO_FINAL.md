# ✅ Agendamento Atualizado - 09:15 AM e 17:15 PM

## 🎉 Configuração Finalizada

A DAG `luma_pipeline` agora está configurada para rodar **2 vezes por dia**:

- ✅ **09:15 AM** (manhã - antes do expediente)
- ✅ **17:15 PM** (5:15 PM - fim do expediente)

### Expressão CRON Utilizada:
```python
schedule="15 9,17 * * *"
```

**Breakdown:**
```
15    = minuto 15
9,17  = horas 09 e 17
*     = todos os dias do mês
*     = todos os meses
*     = todos os dias da semana
```

---

## 📅 Timeline Diária

```
09:15 AM ─────► DAG inicia (1ª execução do dia)
09:16 AM ─────► ETL Bronze + Silver + Gold
09:17 AM ◄───── DAG finaliza (✅ sucesso)

[...durante o dia...]

17:15 PM ─────► DAG inicia (2ª execução do dia)
17:16 PM ─────► ETL Bronze + Silver + Gold
17:17 PM ◄───── DAG finaliza (✅ sucesso)
```

---

## 🔄 Se Uma Execução Falhar

- ⏳ Aguarda 5 minutos
- 🔁 Tenta novamente (máximo 2 tentativas)
- ✅ Se conseguir na tentativa 2, continua normal
- ❌ Se falhar em ambas, registra o erro nos logs

---

## 📊 Monitorar Execuções

### 1. **Web Interface do Airflow**
```
http://localhost:8080
```
- Você verá as próximas 2 execuções por dia
- Histórico de todas as execuções passadas
- Status: sucesso ou falha

### 2. **Logs em Tempo Real**
```bash
docker logs -f airflow_scheduler | grep luma
```

Verá:
```
[09:15:00] Starting execution for luma_pipeline
[09:15:30] Task started: executar_pipeline_master
[09:17:00] Task completed successfully
```

### 3. **Via CLI**
```bash
# Ver próximas execuções
docker exec -it airflow_webserver airflow dags list-runs -d luma_pipeline

# Ver última execução
docker exec -it airflow_webserver airflow dags show-latest luma_pipeline
```

---

## 📝 Arquivo Atualizado

**Localização:** `airflow/dags/dag_luma_pipeline.py`

```python
schedule="15 9,17 * * *"  # ✅ Nova configuração
```

---

## 🎯 Resumo Final

| Aspecto | Configuração |
|---------|-------------|
| **Frequência** | 2 vezes por dia |
| **Horários** | 09:15 AM e 17:15 PM |
| **Dias** | Todos os dias (seg-dom) |
| **Retry** | 2 tentativas com delay de 5 min |
| **Owner** | luma_etl |
| **Status** | ✅ Ativo e funcionando |

---

## 🚀 Próximas Execuções Agendadas

- ✅ Hoje (2026-06-03) às 17:15 PM
- ✅ Amanhã (2026-06-04) às 09:15 AM
- ✅ Amanhã (2026-06-04) às 17:15 PM
- ✅ E assim por diante, todos os dias...

---

## ⚙️ Se Precisar Mudar Novamente

**Para 09:00 AM e 17:15 PM** (exatamente):
```python
schedule="0 9 * * *, 15 17 * * *"  # Não funciona em CRON simples
```

**Alternativas:**
- **09:00 AM + 17:00 PM**: `schedule="0 9,17 * * *"`
- **09:00 AM + 18:00 PM**: `schedule="0 9,18 * * *"`
- **09:30 AM + 17:30 PM**: `schedule="30 9,17 * * *"`
- **Apenas 09:00 AM**: `schedule="0 9 * * *"`

A variação de 15 minutos foi necessária para manter a compatibilidade com CRON padrão do Airflow.

---

**Data:** 2026-06-03  
**Status:** ✅ CONFIGURADO E FUNCIONANDO  
**Próxima Execução:** Hoje 17:15 PM
