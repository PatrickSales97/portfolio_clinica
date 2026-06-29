from airflow import DAG
from airflow.operators.bash import BashOperator # type: ignore
from datetime import datetime, timedelta
import os

# Caminho correto dentro do container
BASE_PATH = "/app/etl"

default_args = {
    "owner": "Patrick",
    "depends_on_past": False,
    "start_date": datetime(2026, 6, 24),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="portfolio_etl",
    start_date=datetime(2026, 6, 29, 12, 30),
    default_args=default_args,
    schedule_interval="30 */6 * * *",
    catchup=False,
    max_active_runs=1
) as dag:

    # =====================
    # BRONZE
    # =====================
    b_conv = BashOperator(
        task_id="bronze_convenios",
        bash_command=f'python "{BASE_PATH}/bronze/bronze_convenios.py"',
    )

    b_pac = BashOperator(
        task_id="bronze_pacientes",
        bash_command=f'python "{BASE_PATH}/bronze/bronze_pacientes.py"',
    )

    b_prof = BashOperator(
        task_id="bronze_profissionais",
        bash_command=f'python "{BASE_PATH}/bronze/bronze_profissionais.py"',
    )

    b_atend = BashOperator(
        task_id="bronze_atendimentos",
        bash_command=f'python "{BASE_PATH}/bronze/bronze_atendimentos.py"',
    )

    b_f_pac = BashOperator(
        task_id="bronze_faltas_pacientes",
        bash_command=f'python "{BASE_PATH}/bronze/bronze_faltas_pacientes.py"',
    )

    b_f_ter = BashOperator(
        task_id="bronze_faltas_terapeutas",
        bash_command=f'python "{BASE_PATH}/bronze/bronze_faltas_terapeutas.py"',
    )

    # =====================
    # SILVER
    # =====================
    s_atend = BashOperator(
        task_id="silver_atendimentos",
        bash_command=f'python "{BASE_PATH}/silver/silver_atendimentos.py"',
    )

    s_f_pac = BashOperator(
        task_id="silver_faltas_pacientes",
        bash_command=f'python "{BASE_PATH}/silver/silver_faltas_pacientes.py"',
    )

    s_f_ter = BashOperator(
        task_id="silver_faltas_terapeutas",
        bash_command=f'python "{BASE_PATH}/silver/silver_faltas_terapeutas.py"',
    )

    # =====================
    # DEPENDÊNCIAS CORRETAS (PIPELINE REAL)
    # =====================

    b_conv >> b_pac >> b_prof >> b_atend >> b_f_pac >> b_f_ter

    b_atend >> s_atend
    b_f_pac >> s_f_pac
    b_f_ter >> s_f_ter