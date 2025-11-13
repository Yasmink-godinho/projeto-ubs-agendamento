from database import start_data_bases # 1. Importa a sua função do arquivo database.py
# (A Pessoa 2 da sua equipe irá adicionar o 'from menu import ...' aqui depois)
from menu import exibir_menu_principal

if __name__ == "__main__":
    print("Iniciando o sistema...")
    
    exibir_menu_principal()
    # 2. Executa a sua função para criar o banco de dados e as tabelas
    start_data_bases()