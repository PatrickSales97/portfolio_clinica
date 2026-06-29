"""
Gerenciador de conexões duplas para sincronizar dados em LOCAL e DOCKER simultaneamente.
Permite executar operações em ambos os bancos sem duplicar código.
"""

import os
import psycopg2 # type: ignore
from pathlib import Path
from dotenv import load_dotenv # type: ignore


BASE_DIR = Path(__file__).resolve().parents[2]


class DualCursor:
    """Wrapper de cursor que funciona em ambos os bancos simultaneamente"""
    
    def __init__(self, cursor_local, cursor_docker):
        self.cursor_local = cursor_local
        self.cursor_docker = cursor_docker
    
    def execute(self, query, params=None):
        """Executa query em ambos os cursores"""
        if self.cursor_local:
            self.cursor_local.execute(query, params)
        if self.cursor_docker:
            self.cursor_docker.execute(query, params)
    
    def executemany(self, query, params_list):
        """Executa múltiplas queries"""
        if self.cursor_local:
            self.cursor_local.executemany(query, params_list)
        if self.cursor_docker:
            self.cursor_docker.executemany(query, params_list)
    
    def fetchone(self):
        """Retorna um registro (do local)"""
        if self.cursor_local:
            return self.cursor_local.fetchone()
        return None
    
    def fetchall(self):
        """Retorna todos os registros (do local)"""
        if self.cursor_local:
            return self.cursor_local.fetchall()
        return []
    
    def close(self):
        """Fecha ambos os cursores"""
        if self.cursor_local:
            self.cursor_local.close()
        if self.cursor_docker:
            self.cursor_docker.close()


class DualConnection:
    """Gerencia 2 conexões PostgreSQL simultaneamente (local e docker)"""
    
    def __init__(self):
        self.conn_local = None
        self.conn_docker = None
        self.cursor_local = None
        self.cursor_docker = None
        self._connect()
    
    def _connect(self):
        """Estabelece conexões com ambos os bancos"""
        # Carrega variáveis de ambiente
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
        
        try:
            self.conn_local = psycopg2.connect(**env_local)
            self.cursor_local = self.conn_local.cursor()
            print("[OK] Conectado ao banco LOCAL")
        except Exception as e:
            print(f"[ERRO] Falha na conexão LOCAL: {e}")
            self.conn_local = None
        
        try:
            self.conn_docker = psycopg2.connect(**env_docker)
            self.cursor_docker = self.conn_docker.cursor()
            print("[OK] Conectado ao banco DOCKER")
        except Exception as e:
            print(f"[ERRO] Falha na conexão DOCKER: {e}")
            self.conn_docker = None
    
    def cursor(self):
        """Retorna um DualCursor compatível com psycopg2.cursor"""
        return DualCursor(self.cursor_local, self.cursor_docker)
    
    def execute(self, query, params=None):
        """
        Executa query em AMBOS os bancos simultaneamente.
        Retorna True se ambos sucessos, False se algum falhar.
        """
        success = True
        
        if self.conn_local:
            try:
                self.cursor_local.execute(query, params)
                print(f"[LOCAL] ✓ Query executada")
            except Exception as e:
                print(f"[LOCAL] ✗ Erro: {e}")
                success = False
        
        if self.conn_docker:
            try:
                self.cursor_docker.execute(query, params)
                print(f"[DOCKER] ✓ Query executada")
            except Exception as e:
                print(f"[DOCKER] ✗ Erro: {e}")
                success = False
        
        return success
    
    def executemany(self, query, params_list):
        """
        Executa múltiplas queries em AMBOS os bancos.
        """
        success = True
        
        if self.conn_local:
            try:
                self.cursor_local.executemany(query, params_list)
                print(f"[LOCAL] ✓ {len(params_list)} registros inseridos")
            except Exception as e:
                print(f"[LOCAL] ✗ Erro: {e}")
                success = False
        
        if self.conn_docker:
            try:
                self.cursor_docker.executemany(query, params_list)
                print(f"[DOCKER] ✓ {len(params_list)} registros inseridos")
            except Exception as e:
                print(f"[DOCKER] ✗ Erro: {e}")
                success = False
        
        return success
    
    def fetchall(self):
        """Retorna dados do banco LOCAL (principal)"""
        if self.conn_local and self.cursor_local:
            return self.cursor_local.fetchall()
        return []
    
    def fetchone(self):
        """Retorna um registro do banco LOCAL"""
        if self.conn_local and self.cursor_local:
            return self.cursor_local.fetchone()
        return None
    
    def commit(self):
        """Commit em ambos os bancos"""
        if self.conn_local:
            self.conn_local.commit()
            print("[LOCAL] ✓ Commit realizado")
        
        if self.conn_docker:
            self.conn_docker.commit()
            print("[DOCKER] ✓ Commit realizado")
    
    def rollback(self):
        """Rollback em ambos os bancos"""
        if self.conn_local:
            self.conn_local.rollback()
            print("[LOCAL] ✓ Rollback realizado")
        
        if self.conn_docker:
            self.conn_docker.rollback()
            print("[DOCKER] ✓ Rollback realizado")
    
    def close(self):
        """Fecha ambas as conexões"""
        if self.cursor_local:
            self.cursor_local.close()
        if self.conn_local:
            self.conn_local.close()
        
        if self.cursor_docker:
            self.cursor_docker.close()
        if self.conn_docker:
            self.conn_docker.close()
        
        print("[OK] Conexões fechadas")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
