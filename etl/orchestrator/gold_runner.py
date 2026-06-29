import subprocess

processos = [

    "etl.gold.gold_kpi_operacional_snapshot",

    "etl.gold.gold_kpi_faturamento_snapshot",

    "etl.gold.gold_kpi_faltas_snapshot"
]

for processo in processos:

    print(f"Executando {processo}")

    subprocess.run(
        ["python", "-m", processo],
        check=True
    )

print("Camada GOLD concluída.")