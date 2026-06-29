CREATE TABLE IF NOT EXISTS silver.atendimentos (
	id_atendimento VARCHAR(50) PRIMARY KEY,
	id_profissional VARCHAR(50),
	id_paciente VARCHAR(50),
	id_convenio VARCHAR(50),
	data_atd DATE,
	hora_atd TIME,
	terapia VARCHAR(100),
	qtd_sessao NUMERIC(10,2),
	valor_sessao NUMERIC(10,2),
	receita_bruta NUMERIC(10,2),
	pgto VARCHAR(100),
	data_pgto DATE,
	motivo_glosa TEXT,
	origem_arquivo VARCHAR(255),
	data_carga TIMESTAMP,
	usuario_execucao VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS silver.faltas_pacientes (
	id_falta_pac VARCHAR(50) PRIMARY KEY,
	data_falta DATE,
	hora_falta TIME,
	id_paciente VARCHAR(50),
	id_convenio VARCHAR(50),
	id_profissional VARCHAR(50),
	terapia VARCHAR(100),
	qtd_sessoes_perdidas NUMERIC(10,2),
	valor_sessao NUMERIC(10,2),
	receita_perdida NUMERIC(10,2),
	pgto VARCHAR(100),
	data_pgto DATE,
	motivo_glosa TEXT,
	origem_arquivo VARCHAR(255),
	data_carga TIMESTAMP,
	usuario_execucao VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS silver.faltas_terapeutas (
	id_falta_ter VARCHAR(50) PRIMARY KEY,
	data_falta DATE,
	hora_falta TIME,
	id_profissional VARCHAR(50),
	qtd_sessoes_perdidas NUMERIC(10,2),
	valor_sessao NUMERIC(10,2),
	receita_perdida NUMERIC(10,2),
	origem_arquivo VARCHAR(255),
	data_carga TIMESTAMP,
	usuario_execucao VARCHAR(100)
);