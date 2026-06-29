import sys
import os
import pandas as pd # type: ignore
from etl.utils.config import get_data_path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from etl.utils.bq_engine import load_to_bq
#from etl.utils.settings import F_ATENDIMENTOS

def main():
    file_path = get_data_path('raw/facts/atendimento.xlsm')
    df = pd.read_excel(file_path)
    print(f"Processando {file_path}")
    
    # Limpeza de nomes de colunas: remove espaços e substitui por underline
    df.columns = [c.strip().replace(" ", "_").replace("/", "_").replace("-", "_") for c in df.columns]
    load_to_bq(df, "atendimentos_raw", "bronze", mode="replace")

if __name__ == "__main__":
    main()