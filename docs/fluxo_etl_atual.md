# Fluxo ETL Atual

```text
Excel
   │
   ▼
Bronze
(PostgreSQL)
   │
   ├──► BigQuery Bronze
   │
   ▼
Silver
(PostgreSQL)
   │
   ├──► BigQuery Silver
   │
   ▼
Gold
(PostgreSQL)
   │
   ├──► BigQuery Gold
   │
   ▼
Power BI
```

---

## Fluxo de Auditoria

```text
Execução ETL
      │
      ▼
audit.etl_run_log (PostgreSQL)
      │
      ▼
audit.etl_run_log (BigQuery)
```

---

## Regras

Todos os ETLs:

1. Criam log RUNNING.
2. Executam transformação.
3. Atualizam PostgreSQL.
4. Atualizam BigQuery.
5. Atualizam auditoria.
6. Encerram como SUCCESS ou ERROR.