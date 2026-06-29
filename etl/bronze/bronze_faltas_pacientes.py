import sys
import os
import pandas as pd # type: ignore

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from etl.utils.bq_engine import load_to_bq
#from etl.utils.settings import F_FALTAS_PAC
from etl.utils.config import get_data_path

def main():
    file_path = get_data_path('raw/facts/faltas_pac.xlsx')
    df = pd.read_excel(file_path)
    print(f"Processando {file_path}")

    # Limpeza de nomes de colunas
    df.columns = [c.strip().replace(" ", "_").replace("/", "_").replace("-", "_") for c in df.columns]
    load_to_bq(df, "faltas_pacientes_raw", "bronze", mode="replace")

if __name__ == "__main__":
    main()