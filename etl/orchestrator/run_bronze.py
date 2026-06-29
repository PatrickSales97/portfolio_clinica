import sys
import os

# Adiciona a raiz do projeto ao path (isso permite importar 'etl')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Agora o import funciona
from etl.utils.logger import setup_logger

def run_bronze():
    logger = setup_logger()
    logger.info("Iniciando carga Bronze...")
    # Aqui viria a lógica que dispara os scripts bronze
    print("Bronze processado com sucesso!")

if __name__ == "__main__":
    run_bronze()