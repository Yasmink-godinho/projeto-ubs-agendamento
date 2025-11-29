from database import conectar  
import sqlite3                 

def adicionar_profissional():
    print("\n--- 1. Cadastrar Novo Profissional ---")
    
    nome = input("Nome completo: ")
    crm = input("CRM do profissional: ")
    especialidade = input("Especialidade: ")

    if not nome or not crm:
        print("Erro: Nome e CRM são campos obrigatórios!")
        return 
    
    conn = None 

    try:
        conn = conectar() 
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO profissionais (nome_completo, crm, especialidade) VALUES (?, ?, ?)",
            (nome, crm, especialidade)
        )
        
        conn.commit() 
        print(f"Profissional '{nome}' cadastrado com sucesso!")
        
    except sqlite3.IntegrityError: 
        print(f"Erro: O CRM '{crm}' já existe no banco de dados.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn: 
            conn.close() 

def listar_profissionais():
    print("\n--- 2. Lista de Profissionais ---")
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM profissionais ORDER BY nome_completo")
        profissionais = cursor.fetchall() 

        if not profissionais:
            print("Nenhum profissional cadastrado.")
            return 

        for p in profissionais:
            print(f"ID: {p['id']} | Nome: {p['nome_completo']} | CRM: {p['crm']} | Especialidade: {p['especialidade']}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()

def atualizar_profissional():
    print("\n--- 3. Atualizar Profissional ---")
    listar_profissionais() 
    
    try:
        id_prof = int(input("Digite o ID do profissional para atualizar: "))
    except ValueError:
        print("Erro: ID inválido. Deve ser um número.")
        return

    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM profissionais WHERE id = ?", (id_prof,))
        profissional = cursor.fetchone() 

        if not profissional:
            print(f"Erro: Profissional com ID {id_prof} não encontrado.")
        else:
            print(f"\nEditando: {profissional['nome_completo']} (Deixe em branco para manter o valor atual)")
            
            novo_nome = input(f"Novo nome completo ({profissional['nome_completo']}): ") or profissional['nome_completo']
            nova_especialidade = input(f"Nova especialidade ({profissional['especialidade']}): ") or profissional['especialidade']
            
            cursor.execute(
                "UPDATE profissionais SET nome_completo = ?, especialidade = ? WHERE id = ?",
                (novo_nome, nova_especialidade, id_prof)
            )
            conn.commit()
            print("Profissional atualizado com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()

def deletar_profissional():
    print("\n--- 4. Deletar Profissional ---")
    listar_profissionais() 
    
    try:
        id_prof = int(input("Digite o ID do profissional a ser deletado: "))
    except ValueError:
        print("Erro: ID inválido. Deve ser um número.")
        return

    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT nome_completo FROM profissionais WHERE id = ?", (id_prof,))
        profissional = cursor.fetchone()

        if not profissional:
            print(f"Erro: Profissional com ID {id_prof} não encontrado.")
        else:
            nome = profissional['nome_completo']
            confirmacao = input(f"Tem certeza que deseja deletar {nome} (ID: {id_prof})? (S/N): ")
            
            if confirmacao.lower() == 's':
                cursor.execute("DELETE FROM profissionais WHERE id = ?", (id_prof,))
                conn.commit()
                print("Profissional deletado com sucesso.")
            else:
                print("Operação cancelada.")
                
    except sqlite3.IntegrityError:
        print(f"Erro: Você não pode deletar {nome}, pois ele(a) está vinculado(a) a consultas existentes.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()