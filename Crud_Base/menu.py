from menu_tarefas import exibir_menu_tarefas
from menu_profissionais import exibir_menu_profissionais  # 👈 adicionado

def exibir_menu_principal():
    while True:
        print("\n========== 🌟 MENU PRINCIPAL 🌟 ==========")
        print("1. 📝 Gerenciar Tarefas")
        print("2. 👨‍⚕️ Gerenciar Profissionais")  # 👈 nova opção
        print("3. 🚪 Sair")
        print("===========================================")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            exibir_menu_tarefas()
        elif opcao == "2":
            exibir_menu_profissionais()  # 👈 chama o menu dos profissionais
        elif opcao == "3":
            print("👋 Saindo... até a próxima!")
            break
        else:
            print("⚠️ Opção inválida! Tente novamente.")
