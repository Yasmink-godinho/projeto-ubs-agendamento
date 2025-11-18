# Importa a função 'conectar' do seu arquivo database.py
from database import conectar  
# Importa a biblioteca sqlite3 para tratar erros específicos (como 'IntegrityError')
import sqlite3 
import datetime            

# --- FUNÇÃO 1: CREATE (Adicionar) ---
def agendar_consulta():
    """Adiciona uma nova consulta ao banco de dados."""
    print("\n-   -- Agendar Nova Consulta ---")
    
    try:
        # 1. Obter dados do usuário
        id_paciente = int(input("Informe o ID do Paciente: "))
        id_profissional = int(input("Informe o ID do Profissional: "))

        data = input("Informe a data no formato (AAAA-MM-DD): ")
        hora = input("Informe a hora no formato (HH:MM): ")

        # 2. Formatar e validar a data/hora
        data_hora = f"{data} {hora}:00"
        datetime.datetime.fromisoformat(data_hora) # Valida o formato


    except ValueError:
        print("Erro: Formato de ID, data ou hora inválido. Use AAAA-MM-DD e HH:MM.")
        return
    except Exception as e:
        # 7. Tratamento de erro genérico (pega qualquer outro problema)
        print(f"Ocorreu um erro nos dados: {e}")
        return
    
    conn = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        # --- VALIDAÇÃO CRÍTICA (Regra de Negócio) ---
        # Antes de agendar, verificar se o profissional já está ocupado
        cursor.execute(
            # O '1' é só para checar existência. É mais rápido que 'SELECT *'
            "SELECT 1 FROM consultas WHERE id_profissional = ? AND data_hora = ? AND status = 'agendada'",
            (id_profissional, data_hora)
        )
        consulta_existente = cursor.fetchone() # Pega um resultado, se houver

        if consulta_existente:
            print("Erro: O profissional já possui uma consulta agendada neste exato horário.")
        else:
            # 4. Se tudo estiver livre, executa o INSERT
            cursor.execute(
                "INSERT INTO consultas (id_paciente, id_profissional, data_hora, status) VALUES (?, ?, ?, 'agendada')",
                (id_paciente, id_profissional, data_hora)
            )
            conn.commit()
            print("✅ Consulta agendada com sucesso!")
            
    except sqlite3.IntegrityError:
        # 5. Tratamento de erro (acontece se o ID do paciente ou profissional não existir - FOREIGN KEY)
        print(f"⚠️ Erro: O Paciente (ID {id_paciente}) ou Profissional (ID {id_profissional}) não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        # 6. Garantir que a conexão feche
        if conn:
            conn.close()


def cancelar_consulta():
    """Muda o status de uma consulta para 'cancelada' (NÃO deleta)."""
    print("\n--- Cancelar Consulta ---")

    listar_consultas_agendadas()

    try:
        id_consulta = int(input("Informe o ID da consulta que você deseja cancelar: "))
    except ValueError:
        print("Erro: ID inválido. Deve ser um número.")
        return

    conn = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        # 1. Verifica se a consulta existe ANTES de tentar cancelar
        cursor.execute("SELECT status FROM consultas WHERE id = ?", (id_consulta,))
        consulta = cursor.fetchone()

        if not consulta:
            print(f"Erro: Consulta com o ID {id_consulta} não encontrada.")
        elif consulta['status'] != 'agendada':
            print(f"Aviso: Esta consulta já está com o status '{consulta['status']}'.")
        else:
            # 2. Executa o UPDATE (muda o status) e não deleta o histórico
            cursor.execute(
                "UPDATE consultas SET status = 'cancelada' WHERE id = ?", (id_consulta,) 
            )
            conn.commit()
            print("Consulta cancelada com sucesso,")
        
    except Exception as e:
        print(f"Ocorreu um erro {e}")
    finally:
        if conn:
            conn.close()
    

# --- FUNÇÃO 3: READ (Listar Todos) ---
def listar_consultas_agendadas():
    """Lista de consultas ativas (para o 'cancelar' funcionar).."""
    print("\n--- Consultas Agendadas ---")
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # 1. Executa a busca, ordenando por nome
        cursor.execute("SELECT id, data_hora, id_paciente, id_profissional FROM consultas WHERE status = 'agendada' ORDER BY data_hora")
        consultas = cursor.fetchall() # Pega todos os resultados

        # 2. Verifica se a lista de consultas está vazia
        if not consultas:
            print("Nenhuma consulta foi agendada.")
            return False # Retorna Falso para o 'cancelar' saber que não há o que cancelar

        # 3. Imprime os resultados usando os nomes das colunas (graças ao 'row_factory')
        for c in consultas: 
            print(f"ID Consulta: {c['id']} | Data: {c['data_hora']} | ID Paciente: {c['id_paciente']} | ID Profissional: {c['id_profissional']}")
        return True # Retorna Verdadeiro se houver consultas

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return False
    finally:
        if conn:
            conn.close()

