from flask import Flask, render_template, request, redirect
from database import conectar
import sqlite3

app = Flask(__name__)

# ----------- PÁGINA INICIAL ------------
@app.route("/")
def index():
    return render_template("base.html")


# ----------- LISTAR CONSULTAS ------------
@app.route("/consultas")
def listar_consultas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM consultas ORDER BY data_hora")
    consultas = cursor.fetchall()
    conn.close()

    return render_template("listar_consultas.html", consultas=consultas)


# ----------- AGENDAR CONSULTA ------------
@app.route("/consultas/agendar", methods=["GET", "POST"])
def agendar_consulta():
    if request.method == "POST":
        id_paciente = request.form["id_paciente"]
        id_profissional = request.form["id_profissional"]
        data = request.form["data"]
        hora = request.form["hora"]

        data_hora = f"{data} {hora}:00"

        conn = conectar()
        cursor = conn.cursor()

        # Impedir conflito
        cursor.execute("""
            SELECT 1 FROM consultas 
            WHERE id_profissional = ? 
            AND data_hora = ?
            AND status = 'agendada'
        """, (id_profissional, data_hora))

        if cursor.fetchone():
            conn.close()
            return "Erro: Profissional já possui consulta neste horário."

        cursor.execute("""
            INSERT INTO consultas (id_paciente, id_profissional, data_hora, status)
            VALUES (?, ?, ?, 'agendada')
        """, (id_paciente, id_profissional, data_hora))

        conn.commit()
        conn.close()

        return redirect("/consultas")

    return render_template("agendar_consulta.html")


# ----------- CANCELAR CONSULTA ------------
@app.route("/consultas/cancelar/<int:id>")
def cancelar_consulta(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE consultas 
        SET status = 'cancelada'
        WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/consultas")


if __name__ == "__main__":
    app.run(debug=True)
    

@app.route("/")
def index():
    return render_template("index.html")

