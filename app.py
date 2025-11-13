from flask import Flask, render_template, request, redirect, url_for
from database import conectar

app = Flask(__name__)

# ------------------- Página inicial -------------------
@app.route('/')
def index():
    return render_template('index.html')

# ------------------- Consultas -------------------
@app.route('/consultas')
def listar_consultas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM consultas")
    consultas = cursor.fetchall()
    conn.close()
    return render_template('consultas/listar.html', consultas=consultas)

@app.route('/consultas/agendar', methods=['GET', 'POST'])
def agendar_consulta():
    if request.method == 'POST':
        paciente_id = request.form['paciente_id']
        profissional_id = request.form['profissional_id']
        data_consulta = request.form['data_consulta']
        hora_consulta = request.form['hora_consulta']

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO consultas (paciente_id, profissional_id, data_consulta, hora_consulta) VALUES (?, ?, ?, ?)",
            (paciente_id, profissional_id, data_consulta, hora_consulta)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('listar_consultas'))

    return render_template('consultas/agendar.html')

@app.route('/consultas/cancelar/<int:id>', methods=['GET', 'POST'])
def cancelar_consulta(id):
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute("DELETE FROM consultas WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_consultas'))

    cursor.execute("SELECT * FROM consultas WHERE id = ?", (id,))
    consulta = cursor.fetchone()
    conn.close()

    return render_template('consultas/cancelar.html', consulta=consulta)


# ------------------- Pacientes (para criar em seguida) -------------------
@app.route('/pacientes')
def listar_pacientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pacientes")
    pacientes = cursor.fetchall()
    conn.close()
    return render_template('pacientes/listar.html', pacientes=pacientes)

@app.route('/pacientes/novo', methods=['GET', 'POST'])
def novo_paciente():
    if request.method == 'POST':
        nome_completo = request.form['nome_completo']
        cpf = request.form['cpf']
        data_nascimento = request.form.get('data_nascimento')
        telefone = request.form.get('telefone')

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pacientes (nome_completo, cpf, data_nascimento, telefone) VALUES (?, ?, ?, ?)",
            (nome_completo, cpf, data_nascimento, telefone)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('listar_pacientes'))

    return render_template('pacientes/criar.html')

@app.route('/pacientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_paciente(id):
    conn = conectar()
    cursor = conn.cursor()
    if request.method == 'POST':
        nome_completo = request.form['nome_completo']
        cpf = request.form['cpf']
        data_nascimento = request.form.get('data_nascimento')
        telefone = request.form.get('telefone')

        cursor.execute("""
            UPDATE pacientes SET nome_completo = ?, cpf = ?, data_nascimento = ?, telefone = ? WHERE id = ?
        """, (nome_completo, cpf, data_nascimento, telefone, id))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_pacientes'))

    cursor.execute("SELECT * FROM pacientes WHERE id = ?", (id,))
    paciente = cursor.fetchone()
    conn.close()

    return render_template('pacientes/editar.html', paciente=paciente)

@app.route('/pacientes/excluir/<int:id>', methods=['GET', 'POST'])
def excluir_paciente(id):
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute("DELETE FROM pacientes WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_pacientes'))

    # Mostrar página de confirmação antes de excluir
    cursor.execute("SELECT * FROM pacientes WHERE id = ?", (id,))
    paciente = cursor.fetchone()
    conn.close()

    return render_template('pacientes/excluir.html', paciente=paciente)





# ------------------- Profissionais (para criar em seguida) -------------------
@app.route('/profissionais')
def listar_profissionais():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profissionais")
    profissionais = cursor.fetchall()
    conn.close()
    return render_template('profissionais/listar.html', profissionais=profissionais)

@app.route('/profissionais/novo', methods=['GET', 'POST'])
def novo_profissional():
    if request.method == 'POST':
        nome_completo = request.form['nome_completo']
        crm = request.form['crm']
        especialidade = request.form['especialidade']

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO profissionais (nome_completo, crm, especialidade) VALUES (?, ?, ?)",
            (nome_completo, crm, especialidade)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('listar_profissionais'))

    return render_template('profissionais/criar.html')

@app.route('/profissionais/editar/<int:id>', methods=['GET', 'POST'])
def editar_profissional(id):
    conn = conectar()
    cursor = conn.cursor()
    if request.method == 'POST':
        nome_completo = request.form['nome_completo']
        crm = request.form['crm']
        especialidade = request.form['especialidade']

        cursor.execute("""
            UPDATE profissionais SET nome_completo = ?, crm = ?, especialidade = ? WHERE id = ?
        """, (nome_completo, crm, especialidade, id))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_profissionais'))

    cursor.execute("SELECT * FROM profissionais WHERE id = ?", (id,))
    profissional = cursor.fetchone()
    conn.close()

    return render_template('profissionais/editar.html', profissional=profissional)

@app.route('/profissionais/excluir/<int:id>', methods=['GET', 'POST'])
def excluir_profissional(id):
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute("DELETE FROM profissionais WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_profissionais'))

    # Mostra uma página de confirmação antes de excluir
    cursor.execute("SELECT * FROM profissionais WHERE id = ?", (id,))
    profissional = cursor.fetchone()
    conn.close()

    return render_template('profissionais/excluir.html', profissional=profissional)



# ------------------- Executar o servidor -------------------
if __name__ == '__main__':
    app.run(debug=True)
