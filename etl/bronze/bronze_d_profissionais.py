import pandas as pd # type: ignore
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from etl.utils.bq_engine import load_to_bq, read_from_bq
#from etl.utils.settings import D_PROFISSIONAL, BQ_PROJECT_ID # Ajuste conforme necessário
from etl.utils.config import get_data_path

def main():
    try:
        file_path = get_data_path('raw/dimensions/profissional.xlsx')
        df = pd.read_excel(file_path)
        print(f"Processando {file_path}")
        
        # Limpeza: força todas as colunas para evitar o ArrowTypeError
        df.columns = [c.lower().replace(" ", "_") for c in df.columns]
        df = df.fillna(0) # Substitui nulos por 0 para evitar erros no BigQuery
        
        load_to_bq(df, "profissionais_raw", "bronze", mode="replace")
        print("Bronze Profissionais: Concluído.")
    except Exception as e:
        print(f"Erro no processamento Bronze: {e}")
        raise e # Isso faz o pipeline_master identificar o erro

if __name__ == "__main__":
    main()