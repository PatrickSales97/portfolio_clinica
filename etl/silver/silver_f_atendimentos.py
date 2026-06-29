import sys
import os
import traceback
import pandas as pd  # type: ignore

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from etl.utils.bq_engine import read_from_bq, load_to_bq


def localizar_coluna(df, nomes):
    mapa = {str(c).strip().lower(): c for c in df.columns}

    for nome in nomes:
        if nome.lower() in mapa:
            return mapa[nome.lower()]

    raise ValueError(f"Coluna não encontrada. Colunas: {list(df.columns)}")


def main():
    try:
        # 🔹 LENDO BRONZE (correto)
        df = read_from_bq("bronze", "atendimentos_raw")

        if df.empty:
            print("Tabela bronze vazia.")
            return

        print("Processando atendimentos (Bronze)")

        # 🔹 COLUNAS
        col_data = localizar_coluna(df, ["DATA", "data"])
        col_hora = localizar_coluna(df, ["HORA", "hora"])

        # 🔥 CORREÇÃO PRINCIPAL (REMOVE .0 DO ID)
        if "id_profissional" in df.columns:
            df["id_profissional"] = pd.to_numeric(
                df["id_profissional"],
                errors="coerce"
            ).astype("Int64")

        # 🔹 DATAS
        df["data_atendimento"] = pd.to_datetime(
            df[col_data],
            errors="coerce"
        ).dt.date

        df["hora_atendimento"] = pd.to_datetime(
            df[col_hora],
            errors="coerce"
        ).dt.strftime("%H:%M")

        # 🔹 REORDENAÇÃO
        cols = (
            ["data_atendimento", "hora_atendimento"]
            + [
                c for c in df.columns
                if c not in ["data_atendimento", "hora_atendimento", col_data, col_hora]
            ]
        )

        df = df[cols]

        # 🔹 LOAD FINAL
        load_to_bq(df, "atendimentos", "silver", mode="replace")

        print("Silver: atendimentos carregado com sucesso.")

    except Exception:
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()