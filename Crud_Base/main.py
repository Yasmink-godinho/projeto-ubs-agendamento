# main.py
from database import inicializar_banco_de_dados
from menu import exibir_menu_principal

if __name__ == "__main__":
    
    # 1. Garante que o banco de dados e as tabelas existam
    inicializar_banco_de_dados()
    
    # 2. Inicia o programa
    exibir_menu_principal()