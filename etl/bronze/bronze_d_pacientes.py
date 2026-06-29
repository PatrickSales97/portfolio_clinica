import pandas as pd # type: ignore
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from etl.utils.bq_engine import load_to_bq, read_from_bq
#from etl.utils.settings import D_PACIENTE, BQ_PROJECT_ID # Ajuste conforme necessário
from etl.utils.config import get_data_path

def main():
    file_path = get_data_path('raw/dimensions/paciente.xlsx')
    df = pd.read_excel(file_path)
    print(f"Processando {file_path}")
    
    # Limpeza básica
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    
    # Carga para a camada Bronze
    load_to_bq(df, "pacientes_raw", "bronze", mode="replace")

if __name__ == "__main__":
    main()