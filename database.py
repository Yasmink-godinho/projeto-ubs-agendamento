import sqlite3
import os

def conectar(): 
    conn = sqlite3.connect("ubs.db", check_same_thread=False) 

    conn.row_factory = sqlite3.Row 

    return conn 
def start_data_bases(): 
    db_existe = os.path.exists("ubs.db") 

    conn = conectar() 
    cursor = conn.cursor() 

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pacientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome_completo TEXT NOT NULL, 
        cpf TEXT NOT NULL UNIQUE, 
        data_nascimento TEXT, 
        telefone TEXT 
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profissionais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_completo TEXT NOT NULL,
        crm TEXT NOT NULL UNIQUE,
        especialidade TEXT 
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consultas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_paciente INTEGER NOT NULL,
        id_profissional INTEGER NOT NULL,
        data_hora DATETIME NOT NULL,
        status TEXT DEFAULT 'agendada',
        
        FOREIGN KEY (id_paciente) REFERENCES pacientes (id) 
            ON DELETE CASCADE, 
        FOREIGN KEY (id_profissional) REFERENCES profissionais (id)
            ON DELETE SET NULL
    );
    """)

    conn.commit() 
    conn.close() 

    if not db_existe:
        print(f'Banco de dados {"ubs.db"} e tabelas criados com sucesso!')
    else:
        print(f'Banco de dados {"ubs.db"} já existe. Conectado.')