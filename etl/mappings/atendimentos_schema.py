# ----------------------------
# SCHEMA MAPPING LAYER - ATENDIMENTOS
# ----------------------------

COLUMN_MAPPING = {
    # Excel → padrão interno
    "data": "data_atd",
    "hora": "hora_atd",
    "id_atendimento": "id_atendimento",
    "id_profissional": "id_profissional",
    "profissional": "profissional",
    "area": "area",
    "id_paciente": "id_paciente",
    "paciente": "paciente",
    "id_convenio": "id_convenio",
    "convenio": "convenio",
    "terapia": "terapia",
    "qtd_sessao": "qtd_sessao",
    "valor_sessao": "valor_sessao",
    "pgto": "pgto",
    "data_pgto": "data_pgto",
    "motivo_glosa": "motivo_glosa"
}

DATE_COLUMNS = ["data_atd", "data_pgto"]

TIME_COLUMNS = ["hora_atd"]

METADATA_COLUMNS = ["origem_arquivo", "data_carga"]