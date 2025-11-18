from database import conectar
import datetime

# 1. Quantidade de profissionais cadastrados
def quantidade_profissionais():
    conn = None # Inicializa a conexão

    try:
        conn = conectar() # Estabelece a conexão com o banco de dados.
        cursor = conn.cursor() # Cria um objeto cursor para executar comandos SQL.

        # Executa a query SQL para contar todas as linhas na tabela 'profissionais'.
        # Uma query SQL é uma instrução escrita em SQL para interagir com o banco de dados. 
        # Ela permite que o usuário solicite, insira, atualize ou exclua dados.
        cursor.execute("SELECT COUNT(*) FROM profissionais") 
        total_profissionais = cursor.fetchone()[0]
        # Pega a primeira (e única) linha do resultado (ex: (15,)).
        # [0] acessa o valor da contagem (ex: 15).

        print(f"\nTotal de Profissionais Cadastrados: {total_profissionais}\n")

    except Exception as e: #captura erros de conexão ou SQL
        print(f"Erro ao buscar total de profissionais: {e}")
    
    finally:
        if conn:
            conn.close() # Fecha a conexão com o banco de dados.

# 2. Quantidade de consultas realizadas
def quantidade_consultas_realizadas():
    conn = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        # Como cada consulta realizada significa 1 atendimento, basta contar todas as consultas com status 'realizada'.
        # Executa a query SQL filtrando as consultas pelo status 'realizada'.
        cursor.execute("SELECT COUNT(*) FROM consultas WHERE status = 'realizada'")
        total_atendimentos = cursor.fetchone()[0]

        print(f"\nTotal de atendimentos (consultas realizadas): {total_atendimentos}\n")

    except Exception as e:
        print(f"Erro ao buscar o total de consultas realizadas: {e}")
    
    finally:
        if conn:
            conn.close()

# 3. Quantidade de consultas canceladas
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

# 4. Relatório por profissional (histórico completo)
def relatorio_por_profissional():
    conn = None
    id_prof = input("\nDigite o ID do profissional: ")
    
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Executa a query SQL para buscar as consultas do profissional.
        # O uso de '?' é para segurança (prevenção de SQL Injection), substituído por (id_prof,)

        # Essa query está dizendo ao banco: "Selecione o ID da consulta, o nome completo do paciente, a data/hora e o status. Faça isso juntando (JOIN) as tabelas consultas e pacientes e filtre apenas as linhas onde o ID do profissional é igual ao valor que vou te passar. Por fim, ordene o resultado pela data."
        cursor.execute("""
            SELECT c.id, p.nome_completo AS paciente, c.data_hora, c.status
            FROM consultas c
            JOIN pacientes p ON c.id_paciente = p.id
            WHERE c.id_profissional = ?
            ORDER BY c.data_hora;
        """, (id_prof,)) # O ID do profissional é passado como uma tupla.
        # Uma tupla é semelhante a uma lista, mas é imutável (não pode ser alterada depois de criada).

        consultas = cursor.fetchall() # Pega todas as linhas retornadas pela consulta.

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

# 5. Relatório por data (consultas do dia)
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