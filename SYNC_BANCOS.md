# 🔄 Sincronização Dupla de Bancos (LOCAL + DOCKER)

## 📋 Resumo

O sistema agora é capaz de **atualizar AMBOS os bancos simultaneamente**:
- **Banco LOCAL** (`localhost:5432`)
- **Banco DOCKER** (`host.docker.internal:5432`)

Isso permite validar que a infra está OK para a migração futura para cloud.

## 🎯 Objetivo

Garantir que os dados são replicados em tempo real entre:
1. Banco local (desenvolvimento manual)
2. Banco do Docker (simulação de ambiente containerizado)

Ambos servem como backup e validação um do outro.

## 🔧 Como Funciona

### Componentes Principais

#### 1. **DualConnection** (`etl/utils/dual_connection.py`)
- Gerencia 2 conexões PostgreSQL simultaneamente
- Executa cada operação em ambos os bancos
- Carrega `.env.local` e `.env.docker` respectivamente

#### 2. **db_connection.py** (modificado)
- Agora oferece 2 modos:
  - `USE_DUAL_CONNECTION=true` → Usa `DualConnection` (padrão)
  - `USE_DUAL_CONNECTION=false` → Usa conexão única (compatibilidade)

## 🚀 Uso

### Modo Automático (Recomendado)
```bash
# Executa ETL atualizando AMBOS os bancos
python -m etl.orchestrator.pipeline_master

# Ou via Airflow DAG
# airflow dags test luma_pipeline
```

A variável `USE_DUAL_CONNECTION` já está setada como `true` por padrão.

### Modo Manual
```python
from etl.utils.db_connection import get_connection

# Retorna DualConnection (atualiza ambos)
conn = get_connection()

# Execute queries normalmente - elas rodam em ambos os bancos
conn.execute("INSERT INTO tabela VALUES (%s, %s)", (val1, val2))
conn.commit()
conn.close()
```

### Desativar Sincronização (Fallback)
```bash
# Executa com uma única conexão (debugging)
export USE_DUAL_CONNECTION=false
python -m etl.orchestrator.pipeline_master
```

## 📊 Saída Esperada

Quando tudo está funcionando:
```
[OK] Conectado ao banco LOCAL
[OK] Conectado ao banco DOCKER
[LOCAL] ✓ Query executada
[DOCKER] ✓ Query executada
[LOCAL] ✓ Commit realizado
[DOCKER] ✓ Commit realizado
```

## ⚠️ Tratamento de Erros

### Se um banco falhar
- O sistema continua e tenta atualizar o outro
- Um log de erro é registrado
- A execução falha apenas se AMBOS os bancos falharem

### Se nenhum banco estiver disponível
- Erro imediato na tentativa de conexão
- Verifique se PostgreSQL está rodando em ambos

## 🔍 Validação

Para validar que os dados foram sincronizados:

```sql
-- Em ambos os bancos (local + docker)
SELECT COUNT(*) FROM bronze.atendimentos_raw;
SELECT COUNT(*) FROM silver.atendimentos;
SELECT COUNT(*) FROM gold.kpi_operacional;
```

Ambas as queries devem retornar o mesmo número de registros.

## 📝 Variáveis de Ambiente

### .env.local
```
DB_HOST=localhost           # LOCAL
DB_PORT=5432
DB_NAME=Luma
DB_USER=postgres
DB_PASSWORD=Luma@4862
```

### .env.docker
```
DB_HOST=host.docker.internal  # Acessível do Docker
DB_PORT=5432
DB_NAME=Luma
DB_USER=postgres
DB_PASSWORD=Luma@4862
```

### Controle de Sincronização
```
USE_DUAL_CONNECTION=true      # Ativa sincronização (padrão)
USE_DUAL_CONNECTION=false     # Desativa (modo debug)
DOCKER_ENV=true               # (Legado) Não mais necessário
```

## 🎓 Próximos Passos

Com a sincronização validada:
1. ✅ Dados replicam corretamente
2. ✅ Infra local está pronta
3. ⏳ Próximo: Integração com BigQuery (cloud)
4. ⏳ Próximo: Power BI apontando para cloud

## 🛠️ Troubleshooting

| Problema | Solução |
|----------|---------|
| Só atualiza banco local | Verifique se `DB_HOST` em `.env.docker` é `host.docker.internal` |
| Conexão recusada (docker) | Confirme que Docker Desktop está rodando |
| Ambos falham | Verifique credenciais em `.env.local` e `.env.docker` |
| Não quer sincronizar | Verifique se `USE_DUAL_CONNECTION=true` |

---

**Criado em:** 2026-06-02  
**Versão:** 1.0 (Sincronização Dupla)
