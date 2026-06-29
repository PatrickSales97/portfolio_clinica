/*create table pacientes(
	id_paciente int primary key,
	nome TEXT(60),
	idconvenio int,
	terapia TEXT(20),
	situacao TEXT(10),
	dt_ativacao date,
	dt_inativacao date
);

create table profissional(
	id_profissional int primary key,
	nome TEXT(60),
	area TEXT(30),
	situacao TEXT(10),
	horas int,
	valor_sessao decimal(10,2),
	valor_mensal decimal(10,2),
	dt_ativacao date,
	dt_inativacao date
);

create table convenio(
	id_convenio int primary key,
	nome TEXT(30),
	situacao TEXT(10),
	valor_sessao decimal(10,2)
);

create table atendimentos(
	id_atendimento TEXT(20),
	data_atd date,
	hora_atd time,
	id_profissional int,
	profissional TEXT(60),
	area TEXT(20),
	id_paciente int,
	paciente TEXT(60),
	id_convenio int,
	convenio TEXT(20),
	terapia TEXT(20),
	qtd_sessao int,
	valor_sessao decimal(10,2),
	pgto char(3),
	data_pgto date,
	motivo_glosa TEXT(100)
);

create table faltas_pac(
	data_falta date,
	hora_falta time,
	id_paciente int,
	nome TEXT(60),
	id_convenio int,
	convenio TEXT(20),
	terapia TEXT(20),
	qtd_sessao int,
	id_profissional int,
	profissional TEXT(60),
	area TEXT(30),
	valor_sessao decimal(10,2),
	pgto char(3),
	data_pgto date,
	motivo_glosa TEXT(100)
);

create table faltas_ter(
	data_falta date,
	hora_falta time,
	id_profissional int,
	nome TEXT(60),
	qtd_sessao int,
	area TEXT(30),
	valor_sessao decimal(10,2)
);*/

CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE SCHEMA IF NOT EXISTS audit;

--------------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS audit.etl_run_log (
    id int,
    processo TEXT(100),
    tabela TEXT(100),
    status TEXT(20),
    data_inicio TIMESTAMP,
    data_fim TIMESTAMP,
    tempo_execucao_seg NUMERIC,
    linhas_inseridas INT,
    linhas_rejeitadas INT,
    mensagem_erro TEXT,
	usuario_execucao TEXT(100)
);

CREATE TABLE IF NOT EXISTS bronze.atendimentos_raw (
    id_atendimento TEXT,
    data_atd DATE,
    hora_atd TEXT,
    id_profissional TEXT,
    profissional TEXT,
    area TEXT,
    id_paciente TEXT,
    paciente TEXT,
    id_convenio TEXT,
    convenio TEXT,
    terapia TEXT,
    qtd_sessao NUMERIC,
    valor_sessao NUMERIC,
    pgto TEXT,
    data_pgto DATE,
    motivo_glosa TEXT,
    origem_arquivo TEXT,
    data_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	usuario_execucao TEXT(100)
);

CREATE TABLE IF NOT EXISTS bronze.faltas_pacientes_raw (
id_falta_pac TEXT(50) PRIMARY KEY,
data_falta DATE,
hora_falta TIME,
id_paciente TEXT(50),
nome TEXT(255),
id_convenio TEXT(50),
convenio TEXT(255),
terapia TEXT(100),
qtd_sessoes_perdidas NUMERIC(10,2),
id_profissional TEXT(50),
profissional TEXT(255),
area TEXT(100),
valor_sessao NUMERIC(10,2),
pgto TEXT(100),
data_pgto DATE,
motivo_glosa TEXT,
origem_arquivo TEXT(255),
data_carga TIMESTAMP,
usuario_execucao TEXT(100)
);

CREATE TABLE IF NOT EXISTS bronze.faltas_terapeutas_raw (
id_falta_ter TEXT(50) PRIMARY KEY,
data_falta DATE,
hora_falta TIME,
id_profissional TEXT(50),
nome TEXT(255),
qtd_sessoes_perdidas NUMERIC(10,2),
area TEXT(100),
valor_sessao NUMERIC(10,2),
origem_arquivo TEXT(255),
data_carga TIMESTAMP,
usuario_execucao TEXT(100)
);

CREATE TABLE bronze.pacientes_raw (
    id_paciente TEXT(50) PRIMARY KEY,
    nome TEXT(255),
    id_convenio TEXT(50),
    terapia TEXT(100),
    situacao TEXT(50),
    dt_ativacao DATE,
    dt_inativacao DATE,
    origem_arquivo TEXT(255),
    data_carga TIMESTAMP,
	usuario_execucao TEXT(100)
);

CREATE TABLE bronze.profissionais_raw (
    id_profissional TEXT(50) PRIMARY KEY,
    nome TEXT(255),
    area TEXT(100),
    situacao TEXT(50),
    horas NUMERIC(10,2),
    valor_sessao NUMERIC(10,2),
    valor_mensal NUMERIC(10,2),
    dt_ativacao DATE,
    dt_inativacao DATE,
    origem_arquivo TEXT(255),
    data_carga TIMESTAMP,
	usuario_execucao TEXT(100)
);

CREATE TABLE bronze.convenios_raw (
    id_convenio TEXT(50) PRIMARY KEY,
    nome TEXT(255),
    situacao TEXT(50),
    valor_sessao NUMERIC(10,2),
    origem_arquivo TEXT(255),
    data_carga TIMESTAMP,
	usuario_execucao TEXT(100)
);

--------------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS silver.atendimentos (
	id_atendimento TEXT(50) PRIMARY KEY,
	id_profissional TEXT(50),
	id_paciente TEXT(50),
	id_convenio TEXT(50),
	data_atd DATE,
	hora_atd TIME,
	terapia TEXT(100),
	qtd_sessao NUMERIC(10,2),
	valor_sessao NUMERIC(10,2),
	receita_bruta NUMERIC(10,2),
	pgto TEXT(100),
	data_pgto DATE,
	motivo_glosa TEXT,
	origem_arquivo TEXT(255),
	data_carga TIMESTAMP,
	usuario_execucao TEXT(100)
);


CREATE TABLE IF NOT EXISTS silver.faltas_pacientes (
	id_falta_pac TEXT(50) PRIMARY KEY,
	data_falta DATE,
	hora_falta TIME,
	id_paciente TEXT(50),
	id_convenio TEXT(50),
	id_profissional TEXT(50),
	terapia TEXT(100),
	qtd_sessoes_perdidas NUMERIC(10,2),
	valor_sessao NUMERIC(10,2),
	receita_perdida NUMERIC(10,2),
	pgto TEXT(100),
	data_pgto DATE,
	motivo_glosa TEXT,
	origem_arquivo TEXT(255),
	data_carga TIMESTAMP,
	usuario_execucao TEXT(100)
);

CREATE TABLE IF NOT EXISTS silver.faltas_terapeutas (
	id_falta_ter TEXT(50) PRIMARY KEY,
	data_falta DATE,
	hora_falta TIME,
	id_profissional TEXT(50),
	qtd_sessoes_perdidas NUMERIC(10,2),
	valor_sessao NUMERIC(10,2),
	receita_perdida NUMERIC(10,2),
	origem_arquivo TEXT(255),
	data_carga TIMESTAMP,
	usuario_execucao TEXT(100)
);
--------------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS gold.kpi_operacional_snapshot (
id INT,
data_referencia DATE,
pacientes_ativos INTEGER,
profissionais_ativos INTEGER,
sessoes_realizadas INTEGER,
sessoes_perdidas_pacientes NUMERIC(10,2),
sessoes_perdidas_terapeutas NUMERIC(10,2),
total_sessoes_operacionais NUMERIC(10,2),
data_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS gold.kpi_faturamento_snapshot (
    id INT,
    data_referencia DATE,
    receita_bruta NUMERIC(12,2),
    receita_glosada NUMERIC(12,2),
    receita_liquida NUMERIC(12,2),
    qtd_sessoes INTEGER,
    ticket_medio NUMERIC(12,2),
    data_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS gold.kpi_faltas_snapshot (
    id INT,
    data_referencia DATE,
    qtd_faltas_pacientes INTEGER,
    qtd_faltas_terapeutas INTEGER,
    sessoes_perdidas_pacientes NUMERIC(10,2),
    sessoes_perdidas_terapeutas NUMERIC(10,2),
    receita_perdida_total NUMERIC(12,2),
    data_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

----------------------------------------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS quality.data_quality_log (
    id INT,
    data_execucao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tabela TEXT(100),
    regra TEXT(200),
    resultado TEXT(20),
    qtd_registros INTEGER,
    observacao TEXT
);

----------------------------------------------------------------------------------------------------

CREATE OR REPLACE VIEW gold.vw_obt_visao_executiva as
WITH fatos_unificadas AS (
    -- 1. Atendimentos
    SELECT
        data_atd AS data_referencia, hora_atd AS hora_referencia, 'Sessao Realizada' AS tipo_evento,
        id_atendimento AS id_registro, id_profissional, id_paciente, id_convenio,
        1 AS qtd_atendimentos, 0 AS qtd_faltas_paciente, 0 AS qtd_faltas_terapeuta,
        0.0 AS valor_falta_paciente, 0.0 AS valor_falta_terapeuta, receita_bruta,
        CASE WHEN LOWER(COALESCE(CAST(pgto AS STRING), '')) = 'glosa' THEN receita_bruta ELSE 0 END AS receita_glosada,
        receita_bruta - (CASE WHEN LOWER(COALESCE(CAST(pgto AS STRING), '')) = 'glosa' THEN receita_bruta ELSE 0 END) AS receita_liquida
    FROM silver.atendimentos

    UNION ALL

    -- 2. Faltas dos Pacientes
    SELECT
        data_falta AS data_referencia, hora_falta AS hora_referencia, 'Falta Paciente' AS tipo_evento,
        id_falta_pac AS id_registro, id_profissional, id_paciente, id_convenio,
        0 AS qtd_atendimentos, qtd_sessoes_perdidas AS qtd_faltas_paciente, 0 AS qtd_faltas_terapeuta,
        CAST(qtd_sessoes_perdidas * valor_sessao AS FLOAT64) AS valor_falta_paciente, 0.0 AS valor_falta_terapeuta,
        0.0 AS receita_bruta, 0.0 AS receita_glosada, 0.0 AS receita_liquida
    FROM silver.faltas_pacientes

    UNION ALL

    -- 3. Faltas dos Terapeutas
    SELECT
        data_falta AS data_referencia, hora_falta AS hora_referencia, 'Falta Terapeuta' AS tipo_evento,
        id_falta_ter AS id_registro, id_profissional, NULL AS id_paciente, NULL AS id_convenio,
        0 AS qtd_atendimentos, 0 AS qtd_faltas_paciente, qtd_sessoes_perdidas AS qtd_faltas_terapeuta,
        0.0 AS valor_falta_paciente, CAST(qtd_sessoes_perdidas * valor_sessao AS FLOAT64) AS valor_falta_terapeuta,
        0.0 AS receita_bruta, 0.0 AS receita_glosada, 0.0 AS receita_liquida
    FROM silver.faltas_terapeutas
),

-- BLINDAGEM: Garante apenas 1 linha por ID pegando a carga mais recente
profissionais_unicos AS (
    SELECT * FROM bronze.profissionais_raw 
    QUALIFY ROW_NUMBER() OVER(PARTITION BY id_profissional ORDER BY data_carga DESC) = 1
),
pacientes_unicos AS (
    SELECT * FROM bronze.pacientes_raw 
    QUALIFY ROW_NUMBER() OVER(PARTITION BY id_paciente ORDER BY data_carga DESC) = 1
),
convenios_unicos AS (
    SELECT * FROM bronze.convenios_raw 
    QUALIFY ROW_NUMBER() OVER(PARTITION BY id_convenio ORDER BY data_carga DESC) = 1
)

SELECT
    f.data_referencia, f.hora_referencia,
    CASE WHEN EXTRACT(HOUR FROM f.hora_referencia) BETWEEN 0 AND 11 THEN 'Manha' ELSE 'Tarde' END AS periodo,
    f.tipo_evento, f.id_registro,
    
    f.id_profissional, dp.nome AS nome_profissional, dp.area AS area_profissional, dp.situacao AS situacao_profissional,
    f.id_paciente, dpa.nome AS nome_paciente, dpa.terapia AS terapia_paciente, dpa.situacao AS situacao_paciente,
    f.id_convenio, dc.nome AS nome_convenio,
    
    f.qtd_atendimentos, f.qtd_faltas_paciente, f.qtd_faltas_terapeuta, f.valor_falta_paciente, f.valor_falta_terapeuta,
    (f.qtd_atendimentos + f.qtd_faltas_paciente + f.qtd_faltas_terapeuta) AS total_sessoes_operacionais,
    f.receita_bruta, f.receita_glosada, f.receita_liquida
FROM fatos_unificadas f
LEFT JOIN profissionais_unicos dp ON CAST(f.id_profissional AS INT64) = CAST(dp.id_profissional AS INT64)
LEFT JOIN pacientes_unicos dpa    ON CAST(f.id_paciente AS INT64) = CAST(dpa.id_paciente AS INT64)
LEFT JOIN convenios_unicos dc     ON CAST(f.id_convenio AS INT64) = CAST(dc.id_convenio AS INT64);

CREATE OR REPLACE VIEW gold.vw_dim_pacientes_ativos AS
SELECT 
    CAST(id_paciente AS INT64) AS id_paciente,
    nome AS nome_paciente,
    terapia AS terapia_paciente,
    CAST(idconvenio AS INT64) AS id_convenio
FROM bronze.pacientes_raw
WHERE LOWER(situacao) = 'ativo';

CREATE OR REPLACE VIEW gold.vw_dim_profissionais_ativos AS
SELECT 
    id_profissional,
    nome AS nome_profissional,
    area AS area_profissional
FROM bronze.profissionais_raw
WHERE situacao = 'Ativo';