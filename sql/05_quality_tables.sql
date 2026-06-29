CREATE TABLE IF NOT EXISTS quality.data_quality_log (
    id SERIAL PRIMARY KEY,
    data_execucao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tabela VARCHAR(100),
    regra VARCHAR(200),
    resultado VARCHAR(20),
    qtd_registros INTEGER,
    observacao TEXT
);