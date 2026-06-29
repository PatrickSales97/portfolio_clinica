# Changelog - Projeto Migração BI Luma

## [2026-05-19]

### Estrutura Inicial
- Criação da estrutura profissional do projeto
- Organização das pastas data/raw/facts e data/raw/dimensions
- Criação da documentação inicial
- Inicialização do versionamento Git

---

### Alterações Banco de Dados
- Inclusão de 2 novas colunas na tabela d_paciente
- Inclusão de 2 novas colunas na tabela d_profissional

---

### Alterações ETL
- Atualização dos scripts d_paciente.py e d_profissional.py para suportar as novas colunas

## [2026-05-20]

### Infraestrutura
- Primeira imagem Docker criada
- ETL executado com sucesso dentro de container
- Refatoração de caminhos absolutos para relativos
- Compatibilidade Docker/Linux implementada
- Configuração de conexão PostgreSQL via host.docker.internal

### Infraestrutura
- Implementado Docker Compose
- Orquestração entre ETL e PostgreSQL
- Implementado readiness check do PostgreSQL
- ETL executando com sucesso via Docker Compose
- Estrutura preparada para futura integração com Airflow

## [2026-05-27]

### Arquitetura de Dados

* Implementação completa da arquitetura Bronze/Silver
* Criação dos schemas:

  * bronze
  * silver
  * gold
  * audit

---

### Camada Bronze

#### Facts

* Implementada tabela bronze.atendimentos_raw
* Implementada tabela bronze.faltas_pacientes_raw
* Implementada tabela bronze.faltas_terapeutas_raw

#### Dimensions

* Implementada tabela bronze.pacientes_raw
* Implementada tabela bronze.profissionais_raw
* Implementada tabela bronze.convenios_raw

---

### ETLs Bronze

* Refatoração completa dos pipelines Bronze
* Implementação de UPSERT incremental
* Tratamento robusto de:

  * datas
  * horários
  * valores nulos
  * NaT
  * tipagem numérica

---

### Auditoria

* Implementada tabela audit.etl_run_log
* Rastreamento de:

  * status execução
  * linhas inseridas
  * linhas rejeitadas
  * mensagens erro
  * tempo execução

---

### Camada Silver

#### Facts

* Implementada silver.atendimentos
* Implementada silver.faltas_pacientes
* Implementada silver.faltas_terapeutas

#### Transformações

* Remoção de redundâncias textuais
* Estruturação analítica
* Cálculo de métricas financeiras
* Criação de receita_bruta
* Criação de receita_perdida

---

### Infraestrutura

* Consolidação do ambiente Docker
* Estrutura preparada para Airflow
* Padronização dos ETLs
* Compatibilidade Linux/Windows estabilizada

---

### Qualidade de Dados

* Correção de problemas de parsing de hora
* Correção de problemas com NaT
* Normalização de horários
* Padronização de datas
* Validação obrigatória de campos críticos

---

### Arquitetura

* Separação oficial das camadas:

  * Raw
  * Trusted
  * Analytical
* Estrutura preparada para futura migração cloud

## [2026-06-01] - GRANDE EVOLUÇÃO: AIRFLOW INTEGRADO

### Infraestrutura
- Implementação do Airflow 2.9.3
- Webserver + Scheduler containerizados
- Docker Compose atualizado para arquitetura completa

### Dependências
- Correção do erro missing dependency: openpyxl
- Inclusão de openpyxl no Dockerfile Airflow
- Ambiente Python unificado entre containers

### Banco de Dados
- Criação/validação dos schemas:
  - gold
  - quality

### Pipeline
- Pipeline master totalmente compatível com Airflow
- Execução via DAG funcionando
- Bronze → Silver → Gold → Quality operacional

### Correções Críticas
- Correção de build context Docker (logs do Airflow excluídos)
- Correção de inicialização do Airflow database
- Correção de execução do scheduler container

### Resultado
- Pipeline totalmente automatizável via Airflow
- Execução manual mantida como fallback

## [2026-06-08]
Airflow
Ajustes de execução em ambiente Docker.
Testes de DAGs e runners.
Projeto
Revisão geral da arquitetura Bronze / Silver / Gold.
Planejamento da sincronização com BigQuery.

## [2026-06-09]
Qualidade
Validação da camada Bronze.
Validação da camada Silver.
Revisão dos mapeamentos.
Correções de tipagem de campos.
Auditoria
Criação do processo centralizado de logging.

## [2026-06-10]
BigQuery
Implementado upload automático para BigQuery em todas as tabelas Bronze.
Implementado upload automático para BigQuery em todas as tabelas Silver.
Criado processo de sincronização da tabela audit.etl_run_log.
Alterado método de carga para WRITE_TRUNCATE.
Validação de sincronização entre PostgreSQL e BigQuery concluída.
Auditoria
Mantido registro simultâneo em PostgreSQL e BigQuery.
Inclusão definitiva do campo usuario_execucao.
Padronização dos status:
RUNNING
SUCCESS
ERROR
Docker
Validação completa da execução via Docker.
Testes de execução manual dos ETLs realizados com sucesso.
Silver
Correção da carga silver.atendimentos.
Implementação de sincronização automática para BigQuery.
Implementação de sincronização automática para audit.
Gold
Definida estratégia de sincronização PostgreSQL → BigQuery.
Padronização dos ETLs Gold para replicação automática.