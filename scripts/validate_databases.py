#!/usr/bin/env python3
"""
Script de Validação Completa - Compara LOCAL vs DOCKER
Valida todas as tabelas: bronze, silver, gold, audit, quality
"""

import psycopg2
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Carregar variáveis de ambiente
load_dotenv(BASE_DIR / ".env.local")
env_local = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

load_dotenv(BASE_DIR / ".env.docker")
env_docker = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

# Lista de tabelas para validar
TABELAS = {
    "BRONZE": [
        "bronze.atendimentos_raw",
        "bronze.convenios_raw",
        "bronze.faltas_pacientes_raw",
        "bronze.faltas_terapeutas_raw",
        "bronze.pacientes_raw",
        "bronze.profissionais_raw",
    ],
    "SILVER": [
        "silver.atendimentos",
        "silver.faltas_pacientes",
        "silver.faltas_terapeutas",
    ],
    "GOLD": [
        "gold.kpi_operacional_snapshot",
        "gold.kpi_faturamento_snapshot",
        "gold.kpi_faltas_snapshot",
        "gold.vw_kpi_operacional",
        "gold.vw_kpi_faturamento",
        "gold.vw_kpi_faltas",
    ],
    "AUDIT": [
        "audit.etl_run_log",
    ],
    "QUALITY": [
        "quality.data_quality_log",
    ]
}

def connect_db(config, name):
    """Conectar ao banco de dados"""
    try:
        conn = psycopg2.connect(**config)
        print(f"✅ Conectado ao banco {name}")
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar em {name}: {e}")
        return None

def get_table_count(conn, schema_table):
    """Obter contagem de registros de uma tabela"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {schema_table}")
        count = cursor.fetchone()[0]
        cursor.close()
        return count
    except Exception as e:
        return None

def generate_report():
    """Gerar relatório de validação"""
    
    print("\n" + "="*80)
    print("VALIDAÇÃO COMPLETA - LOCAL vs DOCKER")
    print("="*80)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Conectar aos bancos
    conn_local = connect_db(env_local, "LOCAL")
    conn_docker = connect_db(env_docker, "DOCKER")
    
    if not conn_local or not conn_docker:
        print("\n❌ Não foi possível conectar em um dos bancos")
        return
    
    # Validar por categoria
    resultados = {}
    
    for categoria, tabelas in TABELAS.items():
        print(f"\n{'─'*80}")
        print(f"📊 {categoria}")
        print(f"{'─'*80}")
        
        resultados[categoria] = []
        
        for tabela in tabelas:
            count_local = get_table_count(conn_local, tabela)
            count_docker = get_table_count(conn_docker, tabela)
            
            if count_local is None and count_docker is None:
                status = "❌ NÃO EXISTE"
                match = "N/A"
            elif count_local is None:
                status = "⚠️  SÓ DOCKER"
                match = f"LOCAL: ❌ | DOCKER: {count_docker:,}"
            elif count_docker is None:
                status = "⚠️  SÓ LOCAL"
                match = f"LOCAL: {count_local:,} | DOCKER: ❌"
            else:
                match_ok = count_local == count_docker
                status = "✅ SINCRONIZADO" if match_ok else "⚠️  DIFERENTE"
                match = f"LOCAL: {count_local:,} | DOCKER: {count_docker:,}"
            
            print(f"  {tabela:<40} [{status}] {match}")
            
            resultados[categoria].append({
                "tabela": tabela,
                "status": status,
                "local": count_local,
                "docker": count_docker,
                "match": count_local == count_docker if count_local and count_docker else False
            })
    
    # Resumo geral
    print(f"\n{'='*80}")
    print("📋 RESUMO GERAL")
    print(f"{'='*80}")
    
    total_tabelas = sum(len(t) for t in TABELAS.values())
    tabelas_sincronizadas = 0
    tabelas_diferentes = 0
    tabelas_ausentes = 0
    
    for categoria, resultados_cat in resultados.items():
        for resultado in resultados_cat:
            if "NÃO EXISTE" in resultado["status"]:
                tabelas_ausentes += 1
            elif "✅" in resultado["status"]:
                tabelas_sincronizadas += 1
            elif "⚠️" in resultado["status"]:
                tabelas_diferentes += 1
    
    print(f"\n✅ Sincronizadas:  {tabelas_sincronizadas}/{total_tabelas}")
    print(f"⚠️  Diferentes:     {tabelas_diferentes}/{total_tabelas}")
    print(f"❌ Ausentes:       {tabelas_ausentes}/{total_tabelas}")
    
    # Status final
    if tabelas_sincronizadas == total_tabelas:
        print(f"\n🎉 RESULTADO: TODOS OS DADOS SINCRONIZADOS!")
    elif tabelas_sincronizadas > tabelas_diferentes:
        print(f"\n⚠️  RESULTADO: MAIORIA SINCRONIZADA, MAS ALGUMAS DIFERENÇAS")
    else:
        print(f"\n❌ RESULTADO: EXISTEM DIFERENÇAS SIGNIFICATIVAS")
    
    # Detalhes por categoria
    print(f"\n{'='*80}")
    print("📈 DETALHES POR CATEGORIA")
    print(f"{'='*80}")
    
    for categoria, resultados_cat in resultados.items():
        sincronizadas = sum(1 for r in resultados_cat if "✅" in r["status"])
        print(f"\n{categoria}: {sincronizadas}/{len(resultados_cat)} tabelas OK")
    
    # Fechar conexões
    conn_local.close()
    conn_docker.close()
    
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    generate_report()
