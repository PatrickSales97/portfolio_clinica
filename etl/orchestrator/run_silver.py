import sys
import os

# Adiciona a raiz do projeto ao path (isso permite que o Python ache a pasta 'etl')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from etl.utils.logger import setup_logger

def run_silver():
    logger = setup_logger()
    logger.info("Iniciando camada Silver...")
    # Aqui você chamaria seus scripts silver, ex:
    # exec(open("etl/silver/silver_f_atendimentos.py").read())
    print("Silver processado com sucesso!")

if __name__ == "__main__":
    run_silver()