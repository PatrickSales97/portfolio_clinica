import subprocess
import sys
import time

from datetime import datetime
from pathlib import Path

import psycopg2 # type: ignore

from etl.utils.logger import setup_logger


logger = setup_logger("run_silver")

BASE_DIR = Path(__file__).resolve().parents[2]

PYTHON_EXEC = sys.executable

SCRIPTS = [

"etl.gold.gold_kpi_operacional_snapshot"

]


def run_script(script):

    print(f"\n[{datetime.now()}] Executando {script}")

    try:
        result = subprocess.run(
        [PYTHON_EXEC, "-m", script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(BASE_DIR),
        timeout=300  # 5 minutos de timeout por script
        )

        print(result.stdout)

        if result.returncode != 0:

            logger.error(f"Erro script: {script}")

            logger.error(result.stderr)

            print(result.stderr)

            return False

        logger.info(f"Script executado com sucesso: {script}")

        print(f"[OK] {script}")

        return True
    
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout: script {script} excedeu 5 minutos")
        print(f"[TIMEOUT] Script {script} foi interrompido por timeout")
        return False


def wait_for_postgres():

    attempts = 0
    max_attempts = 30  # 2.5 minutos (30 * 5 segundos)

    while attempts < max_attempts:

        try:

            from etl.utils.db_connection import get_connection

            conn = get_connection()

            conn.close()

            print("[OK] PostgreSQL disponível.")

            logger.info("PostgreSQL disponível.")

            break

        except Exception as e:

            attempts += 1

            print(f"[AGUARDANDO] PostgreSQL iniciando... (tentativa {attempts}/{max_attempts})")

            logger.warning(
            f"Aguardando PostgreSQL iniciar... Erro: {e}"
            )

            time.sleep(5)
    
    if attempts >= max_attempts:
        print("[ERRO] PostgreSQL não disponível após múltiplas tentativas!")
        logger.error("PostgreSQL não respondeu após múltiplas tentativas")
        raise Exception("Timeout: PostgreSQL não disponível")


def main():

    wait_for_postgres()

    print("\n==========")
    print("INICIANDO Gold")
    print("==========\n")

    for script in SCRIPTS:

        if not run_script(script):

            print("Pipeline Gold interrompido.")

            logger.error(
            "Pipeline Gold interrompido."
            )

            break

    print("\nPipeline Gold finalizado.")

    logger.info("Pipeline Gold finalizado.")


if __name__ == "__main__":

    main()