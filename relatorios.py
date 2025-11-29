from database import conectar
import datetime

def quantidade_profissionais():
    conn = None 

    try:
        conn = conectar() 
        cursor = conn.cursor() 

        cursor.execute("SELECT COUNT(*) FROM profissionais") 
        total_profissionais = cursor.fetchone()[0]

        print(f"\nTotal de Profissionais Cadastrados: {total_profissionais}\n")

    except Exception as e:
        print(f"Erro ao buscar total de profissionais: {e}")
    
    finally:
        if conn:
            conn.close()

def quantidade_consultas_realizadas():
    conn = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM consultas WHERE status = 'realizada'")
        total_atendimentos = cursor.fetchone()[0]

        print(f"\nTotal de atendimentos (consultas realizadas): {total_atendimentos}\n")

    except Exception as e:
        print(f"Erro ao buscar o total de consultas realizadas: {e}")
    
    finally:
        if conn:
            conn.close()

def quantidade_consultas_canceladas():
    conn = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM consultas WHERE status = 'cancelada'")
        total_consultas_canceladas = cursor.fetchone()[0]

        print(f"\nTotal de Consultas Canceladas: {total_consultas_canceladas}\n")

    except Exception as e:
        print(f"Erro ao buscar a quantidade de consultas canceladas: {e}")
    
    finally:
        if conn:
            conn.close()

def relatorio_por_profissional():
    conn = None
    id_prof = input("\nDigite o ID do profissional: ")
    
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id, p.nome_completo AS paciente, c.data_hora, c.status
            FROM consultas c
            JOIN pacientes p ON c.id_paciente = p.id
            WHERE c.id_profissional = ?
            ORDER BY c.data_hora;
        """, (id_prof,)) 

        consultas = cursor.fetchall()

        print("\n===== HISTÓRICO DO PROFISSIONAL =====")
        if consultas:
            for consulta in consultas:
                print(f"Consulta {consulta['id']} | Paciente: {consulta['paciente']} | "
                    f"Data/Hora: {consulta['data_hora']} | Status: {consulta['status']}")
        else:
            print("Nenhuma consulta encontrada para esse profissional.")

        print("\nTotal de consultas desse profissional:", len(consultas))
    
    except Exception as e:
        print(f"Erro ao gerar relatório do profissional {e}")
    
    finally:
        if conn:
            conn.close()

def relatorio_por_data():
    data = input("\nDigite a data (AAAA-MM-DD): ")

    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id, p.nome_completo AS paciente, pr.nome_completo AS profissional, 
               c.data_hora, c.status
            FROM consultas c
            JOIN pacientes p ON c.id_paciente = p.id
            JOIN profissionais pr ON c.id_profissional = pr.id
            WHERE DATE(c.data_hora) = ?
            ORDER BY c.data_hora;
        """, (data,))

        consultas = cursor.fetchall()

        print("\n===== CONSULTAS NA DATA INFORMADA =====")
        if consultas:
            for consulta in consultas:
                print(f"{consulta['data_hora']} | Paciente: {consulta['paciente']} | "
                    f"Profissional: {consulta['profissional']} | Status: {consulta['status']}")
        else:
            print("Nenhuma consulta encontrada nesta data.")

        print("\nTotal de consultas dessa data:", len(consultas))
    
    except Exception as e:
        print(f"Erro ao gerar relatório por data: {e}")
    
    finally:
        if conn:
            conn.close()