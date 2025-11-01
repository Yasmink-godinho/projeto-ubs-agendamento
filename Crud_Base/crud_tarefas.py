# crud_tarefas.py
from database import conectar
import sqlite3 # Importamos para tratar erros

def adicionar_tarefa():
    """Adiciona uma nova tarefa ao banco de dados."""
    titulo = input("Digite o título da tarefa: ")
    if not titulo:
        print("Erro: O título não pode ser vazio.")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO tarefas (titulo) VALUES (?)", (titulo,))
        
        conn.commit()
        print(f"✅ Tarefa '{titulo}' adicionada com sucesso!")
        
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()

def listar_tarefas():
    """Lista todas as tarefas (pendentes e concluídas)."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tarefas ORDER BY id")
        tarefas = cursor.fetchall()

        if not tarefas:
            print("Nenhuma tarefa cadastrada.")
            return

        print("\n--- 📋 Lista de Tarefas ---")
        for tarefa in tarefas:
            print(f"ID: {tarefa['id']} | Título: {tarefa['titulo']} | Status: {tarefa['status']}")
        print("----------------------------")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()

def atualizar_status_tarefa():
    """Muda o status de uma tarefa para 'concluida'."""
    listar_tarefas() # Mostra a lista para o usuário saber o ID
    try:
        id_tarefa = int(input("Digite o ID da tarefa para marcar como 'concluída': "))
    except ValueError:
        print("Erro: ID inválido.")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # 1. Verifica se a tarefa existe
        cursor.execute("SELECT * FROM tarefas WHERE id = ?", (id_tarefa,))
        tarefa = cursor.fetchone()

        if not tarefa:
            print("Erro: Tarefa não encontrada.")
        elif tarefa['status'] == 'concluida':
            print("Aviso: Essa tarefa já estava concluída.")
        else:
            # 2. Atualiza
            cursor.execute("UPDATE tarefas SET status = 'concluida' WHERE id = ?", (id_tarefa,))
            conn.commit()
            print(f"✅ Tarefa '{tarefa['titulo']}' marcada como concluída!")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()

def deletar_tarefa():
    """Remove uma tarefa do banco de dados."""
    listar_tarefas()
    try:
        id_tarefa = int(input("Digite o ID da tarefa que deseja DELETAR: "))
    except ValueError:
        print("Erro: ID inválido.")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # 1. Verifica se a tarefa existe antes de deletar
        cursor.execute("SELECT titulo FROM tarefas WHERE id = ?", (id_tarefa,))
        tarefa = cursor.fetchone()

        if not tarefa:
            print("Erro: Tarefa não encontrada.")
        else:
            titulo = tarefa['titulo'] # Pega o nome para a mensagem de confirmação
            confirmacao = input(f"Tem certeza que deseja deletar '{titulo}' (S/N)? ")
            
            if confirmacao.lower() == 's':
                # 2. Deleta
                cursor.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
                conn.commit()
                print("Tarefa deletada com sucesso.")
            else:
                print("Operação cancelada.")
                
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()