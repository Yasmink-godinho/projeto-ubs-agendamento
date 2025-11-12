# Importa a função 'conectar' do seu arquivo database.py
from database import conectar  
# Importa a biblioteca sqlite3 para tratar erros específicos (como 'IntegrityError')
import sqlite3                 

# --- FUNÇÃO 1: CREATE (Adicionar) ---
def adicionar_profissional():
    """Adiciona um novo profissional ao banco de dados."""
    print("\n--- 1. Cadastrar Novo Profissional ---")
    
    # 1. Obter os dados corretos do usuário
    # (Corrigido: pedia 'nome' e 'cpf', trocado para 'nome_completo' e 'crm')
    nome = input("Nome completo: ")
    crm = input("CRM do profissional: ")
    especialidade = input("Especialidade: ")

    # 2. Validação básica de entrada (requisito do checklist)
    if not nome or not crm:
        print("⚠️ Erro: Nome e CRM são campos obrigatórios!")
        return # Para a função aqui se os dados estiverem inválidos

    conn = None # Inicializa a conexão como Nula (para o 'finally' funcionar)
    try:
        # 3. Conectar ao banco
        conn = conectar() 
        cursor = conn.cursor()
        
        # 4. Executar o SQL com os nomes CORRETOS das colunas
        # (Corrigido: usava 'nome' e 'cpf')
        cursor.execute(
            "INSERT INTO profissionais (nome_completo, crm, especialidade) VALUES (?, ?, ?)",
            (nome, crm, especialidade)
        )
        
        # 5. Salvar (commit) as mudanças no banco
        conn.commit() 
        print(f"✅ Profissional '{nome}' cadastrado com sucesso!")
        
    except sqlite3.IntegrityError: 
        # 6. Tratamento de erro (se o CRM já existir, por causa do 'UNIQUE' no seu BD)
        print(f"⚠️ Erro: O CRM '{crm}' já existe no banco de dados.")
    except Exception as e:
        # 7. Tratamento de erro genérico (pega qualquer outro problema)
        print(f"Ocorreu um erro: {e}")
    finally:
        # 8. Garantir que a conexão seja fechada, mesmo se der erro
        if conn: 
            conn.close() 

# --- FUNÇÃO 2: READ (Listar Todos) ---
def listar_profissionais():
    """Lista todos os profissionais cadastrados."""
    print("\n--- 2. Lista de Profissionais ---")
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # 1. Executa a busca, ordenando por nome
        cursor.execute("SELECT * FROM profissionais ORDER BY nome_completo")
        profissionais = cursor.fetchall() # Pega todos os resultados

        # 2. Verifica se a lista de profissionais está vazia
        if not profissionais:
            print("Nenhum profissional cadastrado.")
            return # Sai da função se a lista estiver vazia

        # 3. Imprime os resultados usando os nomes das colunas (graças ao 'row_factory')
        # (Corrigido: usava índices p[0], p[1] e nomes errados como CPF)
        for p in profissionais:
            print(f"ID: {p['id']} | Nome: {p['nome_completo']} | CRM: {p['crm']} | Especialidade: {p['especialidade']}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()

# --- FUNÇÃO 3: UPDATE (Atualizar) ---
def atualizar_profissional():
    """Atualiza os dados de um profissional existente."""
    print("\n--- 3. Atualizar Profissional ---")
    listar_profissionais() # Boa prática: Mostra a lista para o usuário saber o ID
    
    try:
        # 1. Pede o ID e VALIDA se é um número
        id_prof = int(input("Digite o ID do profissional para atualizar: "))
    except ValueError:
        print("⚠️ Erro: ID inválido. Deve ser um número.")
        return

    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # 2. Verifica se o profissional com esse ID existe ANTES de pedir novos dados
        cursor.execute("SELECT * FROM profissionais WHERE id = ?", (id_prof,))
        profissional = cursor.fetchone() # Pega um único resultado

        if not profissional:
            print(f"⚠️ Erro: Profissional com ID {id_prof} não encontrado.")
        else:
            # 3. Se ele existe, pede os novos dados
            print(f"\nEditando: {profissional['nome_completo']} (Deixe em branco para manter o valor atual)")
            
            # (Corrigido: pedia 'novo_nome', agora pede 'nome_completo')
            novo_nome = input(f"Novo nome completo ({profissional['nome_completo']}): ") or profissional['nome_completo']
            nova_especialidade = input(f"Nova especialidade ({profissional['especialidade']}): ") or profissional['especialidade']
            
            # 4. Executa o UPDATE com os nomes corretos das colunas
            # (Corrigido: usava 'nome=?' e não pedia 'id=?' corretamente)
            cursor.execute(
                "UPDATE profissionais SET nome_completo = ?, especialidade = ? WHERE id = ?",
                (novo_nome, nova_especialidade, id_prof)
            )
            conn.commit()
            print("✅ Profissional atualizado com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()

# --- FUNÇÃO 4: DELETE (Deletar) ---
def deletar_profissional():
    """Deleta um profissional do banco de dados."""
    print("\n--- 4. Deletar Profissional ---")
    listar_profissionais() # Mostra a lista para o usuário saber o ID
    
    try:
        # 1. Pede o ID e VALIDA se é um número
        id_prof = int(input("Digite o ID do profissional a ser deletado: "))
    except ValueError:
        print("⚠️ Erro: ID inválido. Deve ser um número.")
        return

    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # 2. Verifica se o profissional existe ANTES de tentar deletar
        cursor.execute("SELECT nome_completo FROM profissionais WHERE id = ?", (id_prof,))
        profissional = cursor.fetchone()

        if not profissional:
            print(f"⚠️ Erro: Profissional com ID {id_prof} não encontrado.")
        else:
            # 3. Pede confirmação ao usuário (boa prática)
            nome = profissional['nome_completo']
            confirmacao = input(f"Tem certeza que deseja deletar {nome} (ID: {id_prof})? (S/N): ")
            
            if confirmacao.lower() == 's':
                # 4. Executa o DELETE
                cursor.execute("DELETE FROM profissionais WHERE id = ?", (id_prof,))
                conn.commit()
                print("🗑️ Profissional deletado com sucesso.")
            else:
                print("Operação cancelada.")
                
    except sqlite3.IntegrityError:
        # 5. Tratamento de erro (IMPORTANTÍSSIMO!)
        # Isso acontece se o profissional tiver consultas ligadas a ele.
        print(f"⚠️ Erro: Você não pode deletar {nome}, pois ele(a) está vinculado(a) a consultas existentes.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()