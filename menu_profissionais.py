from profissionais import (
    adicionar_profissional,
    listar_profissionais,
    atualizar_profissional,
    deletar_profissional
)

def exibir_menu_profissionais():
    while True:
        print("\n===== MENU DE PROFISSIONAIS =====")
        print("1. Adicionar Profissional")
        print("2. Listar Profissionais")
        print("3. Atualizar Profissional")
        print("4. Deletar Profissional")
        print("0. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if (opcao == "1"):
            adicionar_profissional()
        elif (opcao == "2"):
            listar_profissionais()
        elif (opcao == "3"):
            atualizar_profissional()
        elif (opcao == "4"):
            deletar_profissional()
        elif (opcao == "0"):
            break
        else:
            print("⚠️ Opção inválida! Tente novamente.")
