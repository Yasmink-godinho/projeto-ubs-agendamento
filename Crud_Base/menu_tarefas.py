# menu_tarefas.py
from crud_tarefas import (
    adicionar_tarefa, 
    listar_tarefas, 
    atualizar_status_tarefa, 
    deletar_tarefa
)

def exibir_menu_tarefas():
    """Exibe o submenu para gerenciar tarefas."""
    while True:
        print("\n--- 📝 Menu de Tarefas ---")
        print("1. Adicionar nova tarefa")
        print("2. Listar todas as tarefas")
        print("3. Marcar tarefa como concluída")
        print("4. Deletar tarefa")
        print("5. ↩️ Voltar ao menu principal")
        print("----------------------------")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_tarefa()
        elif opcao == "2":
            listar_tarefas()
        elif opcao == "3":
            atualizar_status_tarefa()
        elif opcao == "4":
            deletar_tarefa()
        elif opcao == "5":
            break
        else:
            print("⚠️ Opção inválida!")