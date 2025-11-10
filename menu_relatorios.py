from relatorios import (
    quantidade_profissionais,
    quantidade_consultas_realizadas,
    quantidade_consultas_canceladas,
    relatorio_por_profissional,
    relatorio_por_data
)

def exibir_menu_relatorios():
    while True:
        print("\n====== MENU DE RELATÓRIOS ======")
        print("1. Quantidade de profissionais cadastrados")
        print("2. Quantidade de pacientes atendidos / consultas realizadas")
        print("3. Quantidade de consultas canceladas")
        print("4. Relatório por profissional (histórico de atendimentos)")
        print("5. Relatório por data (consultas do dia)")
        print("6. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            quantidade_profissionais()
        elif opcao == "2":
            quantidade_consultas_realizadas()
        elif opcao == "3":
            quantidade_consultas_canceladas()
        elif opcao == "4":
            relatorio_por_profissional()
        elif opcao == "5":
            relatorio_por_data()
        elif opcao == "6":
            print("Voltando ao menu principal...")
            break
        else:
            print("Opção inválida. Tente novamente.")