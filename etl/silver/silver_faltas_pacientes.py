import sys
import os
import traceback
import pandas as pd  # type: ignore

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from etl.utils.bq_engine import read_from_bq, load_to_bq
from etl.utils.ids import gerar_id


def localizar_coluna(df, nomes):
    mapa = {str(c).strip().lower(): c for c in df.columns}

    for nome in nomes:
        if nome.lower() in mapa:
            return mapa[nome.lower()]

    raise ValueError(f"Coluna não encontrada. Colunas: {list(df.columns)}")


def main():
    try:
        df = read_from_bq("bronze", "faltas_pacientes_raw")

        if df.empty:
            print("Tabela bronze vazia.")
            return

        print("Processando faltas pacientes (Bronze)")

        col_data = localizar_coluna(df, ["DATA", "data"])
        col_hora = localizar_coluna(df, ["HORA", "hora"])

        df["data_falta"] = pd.to_datetime(df[col_data], errors="coerce").dt.date
        df["hora_falta"] = pd.to_datetime(df[col_hora], errors="coerce").dt.strftime("%H:%M")

        df["id_falta_paciente"] = df["data_falta"].apply(lambda x: gerar_id("PAC", x))

        cols = (
            ["id_falta_paciente", "data_falta", "hora_falta"]
            + [c for c in df.columns if c not in ["id_falta_paciente", "data_falta", "hora_falta", col_data, col_hora]]
        )

        df = df[cols]

        load_to_bq(df, "faltas_pacientes", "silver", mode="replace")

        print("Silver: faltas_pacientes carregado com sucesso.")

    except Exception:
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()