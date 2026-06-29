import subprocess
import sys
import time

from datetime import datetime
from pathlib import Path

import psycopg2  # type: ignore
from dotenv import load_dotenv # type: ignore

from etl.utils.logger import setup_logger

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

logger = setup_logger("run_etl_diario")

PYTHON_EXEC = sys.executable

SCRIPTS = [

    BASE_DIR / "facts" / "f_atendimentos.py",
    BASE_DIR / "facts" / "f_faltas_pac.py",
    BASE_DIR / "facts" / "f_faltas_ter.py",

    BASE_DIR / "dimensions" / "d_convenio.py",
    BASE_DIR / "dimensions" / "d_paciente.py",
    BASE_DIR / "dimensions" / "d_profissional.py",
]


def run_script(script):

    script_path = Path(script)

    if not script_path.exists():

        logger.error(f"Script não encontrado: {script_path}")

        return False

    print(f"[{datetime.now()}] Executando {script_path}")

    result = subprocess.run(
        [PYTHON_EXEC, str(script_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(script_path.parent)
    )

    if result.returncode != 0:

        logger.error(f"Erro script: {script_path}")

        logger.error(result.stderr)

        print(result.stderr)

        return False

    logger.info(f"Script executado com sucesso: {script_path}")

    print(f"[OK] {script_path}")

    return True


def wait_for_postgres():

    while True:

        try:

            from etl.utils.db_connection import get_connection

            conn = get_connection()

            conn.close()

            print("[OK] PostgreSQL disponível.")

            logger.info("PostgreSQL disponível.")

            break

        except psycopg2.OperationalError:

            print("[AGUARDANDO] PostgreSQL iniciando...")

            logger.warning("Aguardando PostgreSQL iniciar...")

            time.sleep(5)


def main():

    wait_for_postgres()

    for script in SCRIPTS:

        if not run_script(script):

            print("ETL interrompido.")

            logger.error("ETL interrompido.")

            break

    print("ETL finalizado.")

    logger.info("ETL finalizado.")


if __name__ == "__main__":

    main()