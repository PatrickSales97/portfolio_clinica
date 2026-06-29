CREATE TABLE IF NOT EXISTS audit.etl_run_log (
    id SERIAL PRIMARY KEY,
    processo VARCHAR(100),
    tabela VARCHAR(100),
    status VARCHAR(20),
    data_inicio TIMESTAMP,
    data_fim TIMESTAMP,
    tempo_execucao_seg NUMERIC,
    linhas_inseridas INT,
    linhas_rejeitadas INT,
    mensagem_erro TEXT,
    usuario_execucao VARCHAR(100)
);

CREATE TABLE bronze.atendimentos_raw (
    id_atendimento VARCHAR(50) PRIMARY KEY,
    data_atd DATE NOT NULL,
    hora_atd TIME NOT NULL,
    id_profissional VARCHAR(50) NOT NULL,
    profissional VARCHAR(255),
    area VARCHAR(100),
    id_paciente VARCHAR(50) NOT NULL,
    paciente VARCHAR(255),
    id_convenio VARCHAR(50),
    convenio VARCHAR(255),
    terapia VARCHAR(100),
    qtd_sessao NUMERIC(10,2),
    valor_sessao NUMERIC(10,2),
    pgto VARCHAR(100),
    data_pgto DATE,
    motivo_glosa TEXT,
    origem_arquivo VARCHAR(255) NOT NULL,
    data_carga TIMESTAMP NOT NULL,
    usuario_execucao VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS bronze.faltas_pacientes_raw (
id_falta_pac VARCHAR(50) PRIMARY KEY,
data_falta DATE,
hora_falta TIME,
id_paciente VARCHAR(50),
nome VARCHAR(255),
id_convenio VARCHAR(50),
convenio VARCHAR(255),
terapia VARCHAR(100),
qtd_sessoes_perdidas NUMERIC(10,2),
id_profissional VARCHAR(50),
profissional VARCHAR(255),
area VARCHAR(100),
valor_sessao NUMERIC(10,2),
pgto VARCHAR(100),
data_pgto DATE,
motivo_glosa TEXT,
origem_arquivo VARCHAR(255),
data_carga TIMESTAMP,
usuario_execucao VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS bronze.faltas_terapeutas_raw (
id_falta_ter VARCHAR(50) PRIMARY KEY,
data_falta DATE,
hora_falta TIME,
id_profissional VARCHAR(50),
nome VARCHAR(255),
qtd_sessoes_perdidas NUMERIC(10,2),
area VARCHAR(100),
valor_sessao NUMERIC(10,2),
pgto VARCHAR(100),
data_pgto DATE,
motivo_glosa TEXT,
origem_arquivo VARCHAR(255),
data_carga TIMESTAMP,
usuario_execucao VARCHAR(100)
);

CREATE TABLE bronze.pacientes_raw (
    id_paciente VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(255),
    id_convenio VARCHAR(50),
    terapia VARCHAR(100),
    situacao VARCHAR(50),
    dt_ativacao DATE,
    dt_inativacao DATE,
    origem_arquivo VARCHAR(255),
    data_carga TIMESTAMP,
	usuario_execucao VARCHAR(100)
);

CREATE TABLE bronze.profissionais_raw (
    id_profissional VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(255),
    area VARCHAR(100),
    situacao VARCHAR(50),
    horas NUMERIC(10,2),
    valor_sessao NUMERIC(10,2),
    valor_mensal NUMERIC(10,2),
    dt_ativacao DATE,
    dt_inativacao DATE,
    origem_arquivo VARCHAR(255),
    data_carga TIMESTAMP,
	usuario_execucao VARCHAR(100)
);

CREATE TABLE bronze.convenios_raw (
    id_convenio VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(255),
    situacao VARCHAR(50),
    valor_sessao NUMERIC(10,2),
    origem_arquivo VARCHAR(255),
    data_carga TIMESTAMP,
	usuario_execucao VARCHAR(100)
);

ALTER TABLE bronze.atendimentos_raw
ADD CONSTRAINT pk_atendimento PRIMARY KEY (id_atendimento);