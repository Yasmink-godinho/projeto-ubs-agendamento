from flask import Flask, render_template, request, redirect, url_for
from database import conectar

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consultas')
def listar_consultas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id, p.nome_completo, pr.nome_completo, c.data_hora, c.status
        FROM consultas c
        JOIN pacientes p ON p.id = c.id_paciente
        JOIN profissionais pr ON pr.id = c.id_profissional
        ORDER BY c.data_hora DESC
    """)
    consultas = cursor.fetchall()
    conn.close()
    return render_template('consultas/listar.html', consultas=consultas)


@app.route('/consultas/agendar', methods=['GET', 'POST'])
def agendar_consulta():
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        id_paciente = request.form['id_paciente']
        id_profissional = request.form['id_profissional']

        data = request.form['data']
        hora = request.form['hora']

        data_hora = f"{data} {hora}:00"

        cursor.execute("""
            INSERT INTO consultas (id_paciente, id_profissional, data_hora, status)
            VALUES (?, ?, ?, 'agendada')
        """, (id_paciente, id_profissional, data_hora))

        conn.commit()
        conn.close()
        return redirect(url_for('listar_consultas'))

    cursor.execute("SELECT id, nome_completo FROM pacientes")
    pacientes = cursor.fetchall()

    cursor.execute("SELECT id, nome_completo FROM profissionais")
    profissionais = cursor.fetchall()

    conn.close()
    return render_template(
        'consultas/agendar.html',
        pacientes=pacientes,
        profissionais=profissionais
    )


@app.route('/consultas/cancelar/<int:id>', methods=['GET', 'POST'])
def cancelar_consulta(id):
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute("UPDATE consultas SET status = 'cancelada' WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_consultas'))

    cursor.execute("SELECT * FROM consultas WHERE id = ?", (id,))
    consulta = cursor.fetchone()
    conn.close()

    return render_template('consultas/cancelar.html', consulta=consulta)


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
        nome = request.form['nome_completo']
        cpf = request.form['cpf']
        nasc = request.form.get('data_nascimento')
        telefone = request.form.get('telefone')

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pacientes (nome_completo, cpf, data_nascimento, telefone)
            VALUES (?, ?, ?, ?)
        """, (nome, cpf, nasc, telefone))

        conn.commit()
        conn.close()
        return redirect(url_for('listar_pacientes'))

    return render_template('pacientes/criar.html')


@app.route('/pacientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_paciente(id):
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome_completo']
        cpf = request.form['cpf']
        nasc = request.form.get('data_nascimento')
        telefone = request.form.get('telefone')

        cursor.execute("""
            UPDATE pacientes
            SET nome_completo=?, cpf=?, data_nascimento=?, telefone=?
            WHERE id=?
        """, (nome, cpf, nasc, telefone, id))

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

    cursor.execute("SELECT * FROM pacientes WHERE id = ?", (id,))
    paciente = cursor.fetchone()
    conn.close()
    return render_template('pacientes/excluir.html', paciente=paciente)


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
        nome = request.form['nome_completo']
        crm = request.form['crm']
        esp = request.form['especialidade']

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO profissionais (nome_completo, crm, especialidade)
            VALUES (?, ?, ?)
        """, (nome, crm, esp))

        conn.commit()
        conn.close()
        return redirect(url_for('listar_profissionais'))

    return render_template('profissionais/criar.html')


@app.route('/profissionais/editar/<int:id>', methods=['GET', 'POST'])
def editar_profissional(id):
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome_completo']
        crm = request.form['crm']
        esp = request.form['especialidade']

        cursor.execute("""
            UPDATE profissionais
            SET nome_completo=?, crm=?, especialidade=?
            WHERE id=?
        """, (nome, crm, esp, id))

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

    cursor.execute("SELECT * FROM profissionais WHERE id = ?", (id,))
    profissional = cursor.fetchone()
    conn.close()
    return render_template('profissionais/excluir.html', profissional=profissional)


@app.route('/pacientes/menu')
def menu_pacientes():
    return render_template('pacientes/menu.html')


@app.route('/profissionais/menu')
def menu_profissionais():
    return render_template('profissionais/menu.html')


@app.route('/consultas/menu')
def menu_consultas():
    return render_template('consultas/menu.html')


@app.route('/relatorios/menu')
def menu_relatorios():
    return render_template('relatorios/menu.html')


@app.route('/relatorios/quantidade-profissionais')
def quantidade_profissionais():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM profissionais")
    total = cursor.fetchone()[0]
    conn.close()
    return render_template('relatorios/quantidade_profissionais.html', total=total)


@app.route('/relatorios/consultas-realizadas')
def consultas_realizadas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM consultas WHERE status='agendada'")
    total = cursor.fetchone()[0]
    conn.close()
    return render_template('relatorios/consultas_realizadas.html', total=total)


@app.route('/relatorios/consultas-canceladas')
def consultas_canceladas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM consultas WHERE status='cancelada'")
    total = cursor.fetchone()[0]
    conn.close()
    return render_template('relatorios/consultas_canceladas.html', total=total)


@app.route('/relatorios/por-profissional', methods=['GET', 'POST'])
def relatorio_por_profissional():
    conn = conectar()
    cursor = conn.cursor()


    if request.method == 'GET':
        cursor.execute("SELECT id, nome_completo FROM profissionais")
        profissionais = cursor.fetchall()
        conn.close()
        return render_template('relatorios/filtrar_profissional.html', profissionais=profissionais)


    profissional_id = request.form.get("id_profissional")

    cursor.execute("""
        SELECT 
            pr.nome_completo AS profissional,
            DATE(c.data_hora) AS data,
            TIME(c.data_hora) AS hora
        FROM consultas c
        JOIN profissionais pr ON pr.id = c.id_profissional
        WHERE c.id_profissional = ?
        ORDER BY c.data_hora DESC
    """, (profissional_id,))

    registros = cursor.fetchall()
    conn.close()

    return render_template('relatorios/por_profissional.html', registros=registros)


@app.route('/relatorios/por-data', methods=['GET', 'POST'])
def relatorio_por_data():
    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.form.get("data_consulta")

        cursor.execute("""
            SELECT c.id, p.nome_completo, pr.nome_completo, c.data_hora, c.status
            FROM consultas c
            JOIN pacientes p ON p.id = c.id_paciente
            JOIN profissionais pr ON pr.id = c.id_profissional
            WHERE DATE(c.data_hora) = ?
            ORDER BY c.data_hora
        """, (data,))

        consultas = cursor.fetchall()
        conn.close()
        return render_template('relatorios/relatorio_data.html', consultas=consultas, data=data)

    conn.close()
    return render_template('relatorios/filtrar_data.html')


if __name__ == '__main__':
    app.run(debug=True)
