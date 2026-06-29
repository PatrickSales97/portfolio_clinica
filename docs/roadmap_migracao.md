# Roadmap de Migração

## Status Atual

### Concluído

* [x] Inventário técnico
* [x] Arquitetura documentada
* [x] Docker funcional
* [x] PostgreSQL operacional
* [x] Camada Bronze concluída
* [x] Camada Silver concluída
* [x] Auditoria implementada
* [x] BigQuery integrado
* [x] Sincronização Bronze → BigQuery
* [x] Sincronização Silver → BigQuery
* [x] Sincronização Audit → BigQuery

---

## Em andamento

* [ ] Sincronização Gold → BigQuery
* [ ] Ajustes finais dos ETLs Gold
* [ ] Revisão dos datasets Gold

---

## Próximos passos

### Fase 1

* Validar todas as tabelas Gold
* Validar quantidades PostgreSQL x BigQuery
* Validar KPIs

### Fase 2

* Integrar DAG completa do Airflow
* Automatizar pipeline fim a fim

### Fase 3

* Conectar Power BI ao BigQuery
* Homologação dos dashboards

### Fase 4

* Descontinuação gradual do PostgreSQL como camada de consumo
* BigQuery como camada principal analítica

### Objetivo Final

```text
Excel
   ↓
Bronze
   ↓
Silver
   ↓
Gold
   ↓
BigQuery
   ↓
Power BI
```