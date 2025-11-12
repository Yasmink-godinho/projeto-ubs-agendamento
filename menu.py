from menu_pacientes import exibir_menu_pacientes
from menu_profissionais import exibir_menu_profissionais
from menu_consultas import exibir_menu_consultas
from menu_relatorios import exibir_menu_relatorios

def exibir_menu_principal():
    while True:
        print("\n===== SISTEMA DE AGENDAMENTO UBS =====")
        print("1. Gerenciar Pacientes")
        print("2. Gerenciar Profissionais")
        print("3. Gerenciar Consultas")
        print("4. Exibir Relatórios")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if (opcao == "1"):
            exibir_menu_pacientes()
        elif (opcao == "2"):
            exibir_menu_profissionais()
        elif (opcao == "3"):
            exibir_menu_consultas()
        elif (opcao == "4"):
            exibir_menu_relatorios()
        elif (opcao == "0"):
            print("Saindo... até a próxima!")
            break
        else:
           print("Opção inválida! Tente novamente.\n") 
