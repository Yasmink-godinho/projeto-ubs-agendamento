# Importa a função 'conectar' do seu arquivo database.py
from database import conectar
# Importa a biblioteca sqlite3 para tratar erros específicos (como 'IntegrityError')  
import sqlite3                 

# --- FUNÇÃO 1: CREATE (Adicionar) ---
def adicionar_paciente():
    """Adiciona um novo paciente ao banco de dados."""
    print("\n--- 1. Cadastrar Novo Paciente ---")

     # 1. Obter os dados corretos do usuário
    # (Corrigido: pedia 'nome' e 'cpf', trocado para 'nome_completo' e 'crm')
    nome = input("Nome completo: ")
    cpf = input("CPF do paciente: ")
    data_nascimento = input("Data de nascimento (AAAA-MM-DD): ")
    telefone = input("Telefone: ")

    # 2. Validação básica de entrada (requisito do checklist)
    if not nome or not cpf:
        print("⚠️ Erro: Nome e CPF são campos obrigatórios!")
        return # Para a função aqui se os dados estiverem inválidos

    conn = None # Inicializa a conexão como Nula (para o 'finally' funcionar)
    try:
         # 3. Conectar ao banco
        conn = conectar()
        cursor = conn.cursor()

        # 4. Executar o SQL com os nomes CORRETOS das colunas
        # (Corrigido: usava 'nome' e 'cpf')
        cursor.execute(
            "INSERT INTO pacientes (nome_completo, cpf, data_nascimento, telefone) VALUES (?, ?, ?, ?)",
            (nome, cpf, data_nascimento, telefone)
        )
         # 5. Salvar (commit) as mudanças no banco
        conn.commit()
        print(f"✅ Paciente '{nome}' cadastrado com sucesso!")

    except sqlite3.IntegrityError:
        # 6. Tratamento de erro (se o CRM já existir, por causa do 'UNIQUE' no seu BD)
        print(f"⚠️ Erro: O CPF '{cpf}' já existe no banco de dados.")
    except Exception as e:
        # 7. Tratamento de erro genérico (pega qualquer outro problema)
        print(f"Ocorreu um erro: {e}")
    finally:
        # 8. Garantir que a conexão seja fechada, mesmo se der erro
        if conn:
            conn.close()

  #--- FUNÇÃO 2: READ (Listar Todos) ---
def listar_pacientes():
    """Lista todos os pacientes cadastrados."""
    print("\n--- 2. Lista de Pacientes ---")
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        # 1. Executa a busca, ordenando por nome
        cursor.execute("SELECT * FROM pacientes ORDER BY nome_completo")
        pacientes = cursor.fetchall() # Pega todos os resultados

        # 2. Verifica se a lista de profissionais está vazia
        if not pacientes:
            print("Nenhum paciente cadastrado.")
            return # Sai da função se a lista estiver vazia

        # 3. Imprime os resultados usando os nomes das colunas (graças ao 'row_factory')
        # (Corrigido: usava índices p[0], p[1] e nomes errados como CPF)
        for p in pacientes:
            print(f"ID: {p['id']} | Nome: {p['nome_completo']} | CPF: {p['cpf']} | Nascimento: {p['data_nascimento']} | Telefone: {p['telefone']}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()

# --- FUNÇÃO 3: UPDATE (Atualizar) ---
def atualizar_paciente():
    """Atualiza os dados de um paciente existente."""
    print("\n--- 3. Atualizar Paciente ---")
    listar_pacientes() # Boa prática: Mostra a lista para o usuário saber o ID

    try:
         # 1. Pede o ID e VALIDA se é um número
        id_pac = int(input("Digite o ID do paciente para atualizar: "))
    except ValueError:
        print("⚠️ Erro: ID inválido. Deve ser um número.")
        return

    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        # 2. Verifica se o profissional com esse ID existe ANTES de pedir novos dados
        cursor.execute("SELECT * FROM pacientes WHERE id = ?", (id_pac,))
        paciente = cursor.fetchone() # Pega um único resultado

        if not paciente:
            print(f"⚠️ Erro: Paciente com ID {id_pac} não encontrado.")
        else:
            # 3. Se ele existe, pede os novos dados
            print(f"\nEditando: {paciente['nome_completo']} (Deixe em branco para manter o valor atual)")
            
             # (Corrigido: pedia 'novo_nome', agora pede 'nome_completo')
            novo_nome = input(f"Novo nome completo ({paciente['nome_completo']}): ") or paciente['nome_completo']
            novo_cpf = input(f"Novo CPF ({paciente['cpf']}): ") or paciente['cpf']
            nova_data = input(f"Nova data de nascimento ({paciente['data_nascimento']}): ") or paciente['data_nascimento']
            novo_tel = input(f"Novo telefone ({paciente['telefone']}): ") or paciente['telefone']

            # 4. Executa o UPDATE com os nomes corretos das colunas
            # (Corrigido: usava 'nome=?' e não pedia 'id=?' corretamente)
            cursor.execute(
                "UPDATE pacientes SET nome_completo = ?, cpf = ?, data_nascimento = ?, telefone = ? WHERE id = ?",
                (novo_nome, novo_cpf, nova_data, novo_tel, id_pac)
            )
            conn.commit()
            print("✅ Paciente atualizado com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()

# --- FUNÇÃO 4: DELETE (Deletar) ---
def deletar_paciente():
    """Deleta um paciente do banco de dados."""
    print("\n--- 4. Deletar Paciente ---")
    listar_pacientes() # Mostra a lista para o usuário saber o ID

    try:
        # 1. Pede o ID e VALIDA se é um número
        id_pac = int(input("Digite o ID do paciente a ser deletado: "))
    except ValueError:
        print("⚠️ Erro: ID inválido. Deve ser um número.")
        return

    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
         
        # 2. Verifica se o profissional existe ANTES de tentar deletar
        cursor.execute("SELECT nome_completo FROM pacientes WHERE id = ?", (id_pac,))
        paciente = cursor.fetchone()

        if not paciente:
            print(f"⚠️ Erro: Paciente com ID {id_pac} não encontrado.")
        # 3. Pede confirmação ao usuário (boa prática)
        else:
            nome = paciente['nome_completo']
            confirmacao = input(f"Tem certeza que deseja deletar {nome} (ID: {id_pac})? (S/N): ")

            if confirmacao.lower() == 's':
                # 4. Executa o DELETE
                cursor.execute("DELETE FROM pacientes WHERE id = ?", (id_pac,))
                conn.commit()
                print("🗑️ Paciente deletado com sucesso.")
            else:
                print("Operação cancelada.")

    except sqlite3.IntegrityError:
        # 5. Tratamento de erro (IMPORTANTÍSSIMO!)
        # Isso acontece se o profissional tiver consultas ligadas a ele
        print(f"⚠️ Erro: Você não pode deletar {nome}, pois ele(a) está vinculado(a) a consultas existentes.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()
