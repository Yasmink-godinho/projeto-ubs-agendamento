from crud_pacientes import (
    adicionar_paciente,
    listar_pacientes,
    atualizar_paciente,
    deletar_paciente
)

def exibir_menu_pacientes():
    while True:
        print("\n===== 🧑‍⚕️ Menu de Pacientes =====")
        print("1. Adicionar Paciente")
        print("2. Listar Pacientes")
        print("3. Atualizar Paciente")
        print("4. Deletar Paciente")
        print("0. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_paciente()
        elif opcao == "2":
            listar_pacientes()
        elif opcao == "3":
            atualizar_paciente()
        elif opcao == "4":
            deletar_paciente()
        elif opcao == "0":
            break
        else:
            print("⚠️ Opção inválida! Tente novamente.")
