from database import conectar  
import sqlite3 
import datetime            


def agendar_consulta():
    print("\n--- Agendar Nova Consulta ---")
    
    try:
        id_paciente = int(input("Informe o ID do Paciente: "))
        id_profissional = int(input("Informe o ID do Profissional: "))

        data = input("Informe a data no formato (AAAA-MM-DD): ")
        hora = input("Informe a hora no formato (HH:MM): ")

        data_hora = f"{data} {hora}:00"
        datetime.datetime.fromisoformat(data_hora)


    except ValueError:
        print("Erro: Formato de ID, data ou hora inválido. Use AAAA-MM-DD e HH:MM.")
        return
    except Exception as e:
        print(f"Ocorreu um erro nos dados: {e}")
        return
    
    conn = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM consultas WHERE id_profissional = ? AND data_hora = ? AND status = 'agendada'",
            (id_profissional, data_hora)
        )
        consulta_existente = cursor.fetchone()

        if consulta_existente:
            print("Erro: O profissional já possui uma consulta agendada neste exato horário.")
        else:
            cursor.execute(
                "INSERT INTO consultas (id_paciente, id_profissional, data_hora, status) VALUES (?, ?, ?, 'agendada')",
                (id_paciente, id_profissional, data_hora)
            )
            conn.commit()
            print("Consulta agendada com sucesso!")
            
    except sqlite3.IntegrityError:
        print(f"Erro: O Paciente (ID {id_paciente}) ou Profissional (ID {id_profissional}) não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()


def cancelar_consulta():
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

        cursor.execute("SELECT status FROM consultas WHERE id = ?", (id_consulta,))
        consulta = cursor.fetchone()

        if not consulta:
            print(f"Erro: Consulta com o ID {id_consulta} não encontrada.")
        elif consulta['status'] != 'agendada':
            print(f"Aviso: Esta consulta já está com o status '{consulta['status']}'.")
        else:
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
    

def listar_consultas_agendadas():
    print("\n--- Consultas Agendadas ---")
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, data_hora, id_paciente, id_profissional FROM consultas WHERE status = 'agendada' ORDER BY data_hora")
        consultas = cursor.fetchall() 

        if not consultas:
            print("Nenhuma consulta foi agendada.")
            return False 

        for c in consultas: 
            print(f"ID Consulta: {c['id']} | Data: {c['data_hora']} | ID Paciente: {c['id_paciente']} | ID Profissional: {c['id_profissional']}")
        return True 

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return False
    finally:
        if conn:
            conn.close()

