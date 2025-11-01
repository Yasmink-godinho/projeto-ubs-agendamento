import sqlite3 # Importa a biblioteca para interagir com o banco de dados SQLite.
import os # Importa a biblioteca de Sistema Operacional, usada para verificar se um arquivo existe.

def conectar(): # Define a função 'conectar' que será usada para abrir a conexão com o banco.
    
    # O 'check_same_thread=False' é uma configuração importante que será útil quando criar a versão web, pois compartilhar a mesma conexão com o banco de dados SQLite entre várias threads
    
    # Cria a conexão com o arquivo "ubs.db". Se o arquivo não existir, ele será criado.
    con = sqlite3.connect("ubs.db", check_same_thread=False) 

    # Isso faz com que os resultados das consultas venham como "dicionários", permitindo acessar por nome da coluna (ex: paciente['nome'])
    
    # Define o 'row_factory' para que os resultados possam ser acessados como dicionários.
    con.row_factory = sqlite3.Row 

    return con # Retorna o objeto de conexão para quem chamou a função.

def start_data_bases(): # Define a função principal que cria a estrutura do banco.
    """
    Cria as tabelas essenciais (pacientes, profissionais, consultas) 
    no banco de dados se elas ainda não existirem.
    """

    # Verifica se o arquivo "ubs.db" já existe no disco e guarda o resultado (True/False).
    db_existe = os.path.exists("ubs.db") 

    con = conectar() # Chama a função 'conectar' e armazena a conexão na variável 'con'.
    cursor = con.cursor() # Cria um 'cursor', objeto usado para executar comandos SQL.

    # Executa o comando SQL para criar a tabela 'pacientes'.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pacientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome_completo TEXT NOT NULL, 
        cpf TEXT NOT NULL UNIQUE, 
        data_nascimento TEXT, 
        telefone TEXT 
    );
    """) # O 'IF NOT EXISTS' impede que o programa quebre se a tabela já existir.

    # Executa o comando SQL para criar a tabela 'profissionais'.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profissionais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_completo TEXT NOT NULL,
        crm TEXT NOT NULL UNIQUE,
        especialidade TEXT 
    );
    """)
    
    # Esta tabela "conecta" as outras duas usando FOREIGN KEY (Chave Estrangeira).
    # Executa o comando SQL para criar a tabela 'consultas'.
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
    # FOREIGN KEY (id_paciente) REFERENCES pacientes (id)
            #ON DELETE CASCADE, /* Se deletar o paciente, deleta a consulta */
        # FOREIGN KEY (id_profissional) REFERENCES profissionais (id)
            #ON DELETE SET NULL /* Se deletar o profissional, a consulta fica sem médico */

    con.commit() # Confirma (salva) todas as transações (CREATE TABLE) no banco de dados.
    con.close() # Fecha a conexão com o banco de dados.

    if not db_existe: # Verifica se o banco de dados acabou de ser criado
        # Imprime uma mensagem de sucesso se o banco foi criado agora.
        print(f'Banco de dados {"ubs.db"} e tabelas criados com sucesso!')
    else:
        # Imprime uma mensagem de aviso se o banco já existia.
        print(f'Banco de dados {"ubs.db"} já existe. Conectado.')