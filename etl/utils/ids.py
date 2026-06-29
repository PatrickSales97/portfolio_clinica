import uuid
import random

def gerar_id(prefixo, data_obj):
    # Formato: PREFIXO-AAAAMMDD-XXXX (XXXX aleatório de 0000 a 9999)
    data_str = data_obj.strftime("%Y%m%d")
    sufixo = f"{random.randint(0, 9999):04d}"
    return f"{prefixo}-{data_str}-{sufixo}"