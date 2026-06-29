from pathlib import Path

# ==========================================================
# BASE DO PROJETO
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ==========================================================
# DIRETÓRIOS
# ==========================================================

DATA_DIR = BASE_DIR / "data"

RAW_DIR = DATA_DIR / "raw"

FACTS_DIR = RAW_DIR / "facts"

DIMENSIONS_DIR = RAW_DIR / "dimensions"

LOG_DIR = BASE_DIR / "logs"

# ==========================================================
# ARQUIVOS FACT
# ==========================================================

F_ATENDIMENTOS = FACTS_DIR / "atendimento.xlsm"

F_FALTAS_PAC = FACTS_DIR / "faltas_pac.xlsx"

F_FALTAS_TER = FACTS_DIR / "faltas_ter.xlsx"

# ==========================================================
# ARQUIVOS DIMENSION
# ==========================================================

D_PACIENTE = DIMENSIONS_DIR / "paciente.xlsx"

D_PROFISSIONAL = DIMENSIONS_DIR / "profissional.xlsx"

D_CONVENIO = DIMENSIONS_DIR / "convenio.xlsx"

# etl/utils/settings.py

BQ_PROJECT_ID = "clinica-500413"