import sys
import os
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Imports de todos os scripts Bronze
from etl.bronze.bronze_atendimentos import main as b_atend
from etl.bronze.bronze_d_convenios import main as b_conv
from etl.bronze.bronze_d_pacientes import main as b_pacientes
from etl.bronze.bronze_d_profissionais import main as b_prof
from etl.bronze.bronze_faltas_pacientes import main as b_fpac
from etl.bronze.bronze_faltas_terapeutas import main as b_fter

# Imports de todos os scripts Silver
from etl.silver.silver_f_atendimentos import main as s_atend
from etl.silver.silver_faltas_pacientes import main as s_fpac
from etl.silver.silver_faltas_terapeutas import main as s_fter

def run_pipeline():
    steps = [
        ("Bronze Atendimentos", b_atend),
        ("Bronze Convenios", b_conv),
        ("Bronze Pacientes", b_pacientes),
        ("Bronze Profissionais", b_prof),
        ("Bronze Faltas Pac", b_fpac),
        ("Bronze Faltas Ter", b_fter),
        ("Silver Atendimentos", s_atend),
        ("Silver Faltas Pac", s_fpac),
        ("Silver Faltas Ter", s_fter)
    ]
    
    total_steps = len(steps)
    
    for i, (name, func) in enumerate(steps, 1):
        percent = int((i / total_steps) * 100)
        try:
            print(f"Executando: {name}... {percent}%")
            func()
        except Exception:
            print(f"\n!!! ERRO CRÍTICO EM: {name} !!!")
            traceback.print_exc()
            sys.exit(1) # O pipeline para aqui se der erro em qualquer etapa
            
    print("\nPIPELINE FINALIZADO COM SUCESSO! 100%")

if __name__ == "__main__":
    run_pipeline()