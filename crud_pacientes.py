from database import conectar
import sqlite3                 

def adicionar_paciente():
    print("\n--- 1. Cadastrar Novo Paciente ---")

    nome = input("Nome completo: ")
    cpf = input("CPF do paciente: ")
    data_nascimento = input("Data de nascimento (AAAA-MM-DD): ")
    telefone = input("Telefone: ")

    if not nome or not cpf:
        print("Erro: Nome e CPF são campos obrigatórios!")
        return

    conn = None 
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO pacientes (nome_completo, cpf, data_nascimento, telefone) VALUES (?, ?, ?, ?)",
            (nome, cpf, data_nascimento, telefone)
        )
         
        conn.commit()
        print(f"Paciente '{nome}' cadastrado com sucesso!")

    except sqlite3.IntegrityError:
        print(f"Erro: O CPF '{cpf}' já existe no banco de dados.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()

def listar_pacientes():
    print("\n--- 2. Lista de Pacientes ---")
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM pacientes ORDER BY nome_completo")
        pacientes = cursor.fetchall()

        if not pacientes:
            print("Nenhum paciente cadastrado.")
            return

        for p in pacientes:
            print(f"ID: {p['id']} | Nome: {p['nome_completo']} | CPF: {p['cpf']} | Nascimento: {p['data_nascimento']} | Telefone: {p['telefone']}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()

def atualizar_paciente():
    print("\n--- 3. Atualizar Paciente ---")
    listar_pacientes() 

    try:
        id_pac = int(input("Digite o ID do paciente para atualizar: "))
    except ValueError:
        print("Erro: ID inválido. Deve ser um número.")
        return

    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM pacientes WHERE id = ?", (id_pac,))
        paciente = cursor.fetchone() 

        if not paciente:
            print(f"Erro: Paciente com ID {id_pac} não encontrado.")
        else:

           print(f"\nEditando: {paciente['nome_completo']} (Deixe em branco para manter o valor atual)")
            
            novo_nome = input(f"Novo nome completo ({paciente['nome_completo']}): ") or paciente['nome_completo']
            novo_cpf = input(f"Novo CPF ({paciente['cpf']}): ") or paciente['cpf']
            nova_data = input(f"Nova data de nascimento ({paciente['data_nascimento']}): ") or paciente['data_nascimento']
            novo_tel = input(f"Novo telefone ({paciente['telefone']}): ") or paciente['telefone']

            cursor.execute(
                "UPDATE pacientes SET nome_completo = ?, cpf = ?, data_nascimento = ?, telefone = ? WHERE id = ?",
                (novo_nome, novo_cpf, nova_data, novo_tel, id_pac)
            )
            conn.commit()
            print("Paciente atualizado com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()

def deletar_paciente():
    print("\n--- 4. Deletar Paciente ---")
    listar_pacientes() 
    try:
        id_pac = int(input("Digite o ID do paciente a ser deletado: "))
    except ValueError:
        print("Erro: ID inválido. Deve ser um número.")
        return

    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
         
        cursor.execute("SELECT nome_completo FROM pacientes WHERE id = ?", (id_pac,))
        paciente = cursor.fetchone()

        if not paciente:
            print(f"Erro: Paciente com ID {id_pac} não encontrado.")
        else:
            nome = paciente['nome_completo']
            confirmacao = input(f"Tem certeza que deseja deletar {nome} (ID: {id_pac})? (S/N): ")

            if confirmacao.lower() == 's':
                cursor.execute("DELETE FROM pacientes WHERE id = ?", (id_pac,))
                conn.commit()
                print("Paciente deletado com sucesso.")
            else:
                print("Operação cancelada.")

    except sqlite3.IntegrityError:
        print(f"Erro: Você não pode deletar {nome}, pois ele(a) está vinculado(a) a consultas existentes.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()
