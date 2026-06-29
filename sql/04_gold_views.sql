CREATE OR REPLACE VIEW gold.vw_kpi_faturamento AS
SELECT
	data_atd,
	id_profissional,
	id_convenio,
	COUNT(id_atendimento) AS qtd_sessoes,
	SUM(receita_bruta) AS receita_bruta,
	SUM(
	CASE
	WHEN LOWER(COALESCE(pgto, '')) = 'glosa'
	THEN receita_bruta
	ELSE 0
	END
	) AS receita_glosada,
	SUM(receita_bruta)
	-
	SUM(
	CASE
	WHEN LOWER(COALESCE(pgto, '')) = 'glosa'
	THEN receita_bruta
	ELSE 0
	END
	) AS receita_liquida,
	ROUND(
	(
	SUM(receita_bruta)
	-
	SUM(
	CASE
	WHEN LOWER(COALESCE(pgto, '')) = 'glosa'
	THEN receita_bruta
	ELSE 0
	END
	)
	)
	/
	NULLIF(COUNT(id_atendimento), 0),
	2
	) AS ticket_medio
FROM silver.atendimentos
GROUP BY
	data_atd,
	id_profissional,
	id_convenio
;

CREATE OR REPLACE VIEW gold.vw_kpi_faltas AS
SELECT
'PACIENTE' AS tipo_falta,
data_falta,
id_profissional,
id_convenio,
COUNT(id_falta_pac) AS qtd_faltas,
SUM(qtd_sessoes_perdidas) AS qtd_sessoes_perdidas,
SUM(receita_perdida) AS receita_perdida
FROM silver.faltas_pacientes
GROUP BY
data_falta,
id_profissional,
id_convenio

UNION ALL

SELECT
'TERAPEUTA' AS tipo_falta,
data_falta,
id_profissional,
NULL AS id_convenio,
COUNT(id_falta_ter) AS qtd_faltas,
SUM(qtd_sessoes_perdidas) AS qtd_sessoes_perdidas,
SUM(receita_perdida) AS receita_perdida
FROM silver.faltas_terapeutas
GROUP BY
data_falta,
id_profissional;

CREATE OR REPLACE VIEW gold.vw_kpi_operacional AS
SELECT
  data_atd AS data_referencia,
  COUNT(DISTINCT id_atendimento) AS sessoes_realizadas,
  (
    SELECT COUNT(*)
    FROM silver.faltas_pacientes fp
    WHERE fp.data_falta = a.data_atd
  ) AS sessoes_perdidas_pacientes,
  (
    SELECT COUNT(*)
    FROM silver.faltas_terapeutas ft
    WHERE ft.data_falta = a.data_atd
  ) AS sessoes_perdidas_terapeutas
FROM silver.atendimentos a
GROUP BY data_atd;

CREATE TABLE IF NOT EXISTS gold.kpi_operacional_snapshot (
id SERIAL PRIMARY KEY,
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
    id SERIAL PRIMARY KEY,
    data_referencia DATE,
    receita_bruta NUMERIC(12,2),
    receita_glosada NUMERIC(12,2),
    receita_liquida NUMERIC(12,2),
    qtd_sessoes INTEGER,
    ticket_medio NUMERIC(12,2),
    data_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS gold.kpi_faltas_snapshot (
    id SERIAL PRIMARY KEY,
    data_referencia DATE,
    qtd_faltas_pacientes INTEGER,
    qtd_faltas_terapeutas INTEGER,
    sessoes_perdidas_pacientes NUMERIC(10,2),
    sessoes_perdidas_terapeutas NUMERIC(10,2),
    receita_perdida_total NUMERIC(12,2),
    data_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);