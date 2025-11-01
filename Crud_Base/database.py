# database.py
import sqlite3
import os

# Nome do arquivo do banco de dados
DB_FILE = "tarefas.db"

def conectar():
    """Conecta ao banco de dados SQLite."""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_banco_de_dados():
    """Cria as tabelas se elas não existirem."""
    db_existe = os.path.exists(DB_FILE)
    
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de tarefas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        status TEXT DEFAULT 'pendente'
    );
    """)

    # Tabela de profissionais
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profissionais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT UNIQUE NOT NULL,
        especialidade TEXT
    );
    """)

    conn.commit()
    conn.close()
    
    if not db_existe:
        print(f"Banco de dados '{DB_FILE}' criado com sucesso.")
