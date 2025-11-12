from crud_consultas import(
    agendar_consulta,
    cancelar_consulta,
    listar_consultas_agendadas
)
from crud_pacientes import (
    listar_pacientes
)

from crud_profissionais import (
    listar_profissionais
)

def exibir_menu_consultas():
     while True:
        print("\n===== 🗓️ Menu de Consultas =====")
        print("1. Agendar nova consulta")
        print("2. Cancelar consulta")
        print("3. Listar consultas agendadas")
        print("0. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\n--- Agendando Nova Consulta ---")
            
            print("\nPacientes disponíveis:")
            listar_pacientes() 
            print("\nProfissionais disponíveis:")
            listar_profissionais()

            agendar_consulta()
        elif opcao == "2":
            cancelar_consulta()
        elif opcao == "3":
            listar_consultas_agendadas()
        elif opcao == "0":
            break
        else:
            print("⚠️ Opção inválida! Tente novamente.")
