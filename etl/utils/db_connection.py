import os
from pathlib import Path
from dotenv import load_dotenv # type: ignore
import psycopg2 # type: ignore

BASE_DIR = Path(__file__).resolve().parents[2]

# Configuração: desativar sincronização dupla por enquanto (modo seguro)
# TODO: Implementar sincronização dupla sem deadlock futuramente
USE_DUAL_CONNECTION = os.getenv("USE_DUAL_CONNECTION", "false").lower() == "true"

ENV_FILE = ".env.docker" if os.getenv("DOCKER_ENV") == "true" else ".env.local"

load_dotenv(BASE_DIR / ENV_FILE)

def get_connection():
    """
    Retorna conexão única ou dupla conforme configurado.
    USE_DUAL_CONNECTION=true: Sincroniza LOCAL e DOCKER (experimental)
    USE_DUAL_CONNECTION=false: Usa apenas a conexão padrão (padrão seguro)
    """
    if USE_DUAL_CONNECTION:
        from etl.utils.dual_connection import DualConnection
        return DualConnection()
    
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )