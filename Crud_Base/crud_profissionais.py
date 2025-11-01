import sqlite3
from database import conectar

def adicionar_profissional():
    conexao = conectar()
    cursor = conexao.cursor()
    nome = input("Nome do profissional: ")
    cpf = input("CPF do profissional: ")
    especialidade = input("Especialidade: ")
    cursor.execute("INSERT INTO profissionais (nome, cpf, especialidade) VALUES (?, ?, ?)", (nome, cpf, especialidade))
    conexao.commit()
    conexao.close()
    print("✅ Profissional adicionado com sucesso!")

def listar_profissionais():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM profissionais")
    profissionais = cursor.fetchall()
    conexao.close()
    print("\n===== Lista de Profissionais =====")
    for p in profissionais:
        print(f"ID: {p[0]} | Nome: {p[1]} | CPF: {p[2]} | Especialidade: {p[3]}")

def atualizar_profissional():
    conexao = conectar()
    cursor = conexao.cursor()
    id_prof = input("ID do profissional para atualizar: ")
    novo_nome = input("Novo nome: ")
    nova_especialidade = input("Nova especialidade: ")
    cursor.execute("UPDATE profissionais SET nome=?, especialidade=? WHERE id=?", (novo_nome, nova_especialidade, id_prof))
    conexao.commit()
    conexao.close()
    print("✏️ Profissional atualizado com sucesso!")

def deletar_profissional():
    conexao = conectar()
    cursor = conexao.cursor()
    id_prof = input("ID do profissional a ser deletado: ")
    cursor.execute("DELETE FROM profissionais WHERE id=?", (id_prof,))
    conexao.commit()
    conexao.close()
    print("🗑️ Profissional deletado com sucesso!")
