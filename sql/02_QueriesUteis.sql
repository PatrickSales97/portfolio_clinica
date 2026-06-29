
select 
	area,
	sum(qtd_sessao) as Qtd_Sessoes,
	sum(valor_sessao) as Valor_Total
from atendimentos
where 
	id_convenio = 1
	--and area in ('Fisio','Ed Fisica')
	--and data_atd < '2026-01-01'
group by area
order by Valor_Total desc;

---------------------------------------------------------------------------------------------------------------------------------------------------------

select
	profissional,
	sum(qtd_sessao) as hist_total_atdmntos,
	sum(qtd_sessao) - (select count(*) from atendimentos) as diferenca_total_atdmntos,
	(select count(*) from atendimentos) as total_atdmntos_psico	
from atendimentos
group by profissional
order by hist_total_atdmntos desc;

---------------------------------------------------------------------------------------------------------------------------------------------------------

select
	sum(qtd_sessao) as total_atendimentos
from atendimentos
where area = 'Psicologia'
	and terapia <> 'AT';

---------------------------------------------------------------------------------------------------------------------------------------------------------

select
	sum(qtd_sessao) as total_atendimentos
from atendimentos

select
	sum(qtd_sessao) as total_faltas
from faltas_pac;

select
	sum(qtd_sessao) as total_faltas
from faltas_ter;

---------------------------------------------------------------------------------------------------------------------------------------------------------

insert into atendimentos (id_atendimento,
	data_atd,
	hora_atd,
	id_profissional,
	profissional,
	area,
	id_paciente,
	paciente,
	id_convenio,
	convenio,
	terapia,
	qtd_sessao,
	valor_sessao,
	pgto,
	data_pgto,
	motivo_glosa)
values(
	'ATD-20260127-MZ41',
	'2026-01-27',
	'11:00:00',
	6,
	'Lorrane Alves de Oliveira',
	'Psicologia',
	122,
	'AT Daniel Salzgeber Bezerra Bordotti Zanetin',
	1,
	'Cassi',
	'AT',
	1,
	170.00,
	null,
	null,
	null
);

---------------------------------------------------------------------------------------------------------------------------------------------------------

select
	32 as Total_Sessoes_Mes,
	sum(a.qtd_sessao) as Sessoes_Realizadas,
	sum(f.qtd_sessao) as Sessoes_Perdidas,
	32.0 / sum(f.qtd_sessao) as Media_Faltas
from atendimentos a
join faltas_pac f
on f.id_paciente = a.id_paciente
where a.id_paciente = 26;

---------------------------------------------------------------------------------------------------------------------------------------------------------

select
	profissional,
	sum(qtd_sessao) as hist_total_atdmntos,
	sum(qtd_sessao) - (select count(*) from atendimentos where area = 'Psicologia' and terapia <> 'AT') as diferenca_total_atdmntos,
	(select count(*) from atendimentos where area = 'Psicologia' and terapia <> 'AT') as total_atdmntos_psico	
from atendimentos
where area = 'Psicologia'
	and profissional in ('Sandra Fabiano', 'Dayane Alves de Lima', 'Tabata Mickaelle Alves Santos da Silva', 'Bruna Marchiori Franco Bueno')
	and terapia <> 'AT'
group by profissional
order by hist_total_atdmntos desc;

---------------------------------------------------------------------------------------------------------------------------------------------------------

select
	count(*) as total_ABA
from pacientes
where terapia = 'ABA';