import sys
import os
import pandas as pd # type: ignore

# Garante que o Python encontre a raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from etl.utils.bq_engine import load_to_bq
from etl.utils.config import get_data_path
#from etl.utils.settings import F_FALTAS_TER

def main():
    file_path = get_data_path('raw/facts/faltas_ter.xlsx')
    df = pd.read_excel(file_path)
    print(f"Processando {file_path}")

    # 2. LIMPEZA TOTAL: Remove espaços em branco, quebras, troca espaços por underscore e tudo em minúsculo
    # Isso resolve o erro 'data ' e 'NOME '
    df.columns = [
        c.strip().replace(" ", "_").replace(",", "").replace("/", "_").lower() 
        for c in df.columns
    ]
    
    # 3. Carga: Corrigido o nome da tabela para 'faltas_terapeutas'
    # Antes estava 'atendimentos', o que causava erro de lógica e conflito
    load_to_bq(df, "faltas_terapeutas_raw", "bronze", mode="replace")
    print("Bronze: faltas_terapeutas carregada com sucesso.")

if __name__ == "__main__":
    main()