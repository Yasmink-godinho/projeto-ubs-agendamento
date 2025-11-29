from database import start_data_bases
from menu import exibir_menu_principal

if __name__ == "__main__":
    print("Iniciando o sistema...")
    
    exibir_menu_principal()
    start_data_bases()