from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Muestra los números disponibles
@app.route("/")
def mostrar_numeros():
    conn = sqlite3.connect("rifa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT numero, estado, comprador, pagado FROM rifas")
    numeros = cursor.fetchall()
    conn.close()

    # Formatear los números con tres cifras (ejemplo: 001, 005, 010)
    numeros_formateados = [{
        'numero': f'{numero[0]:03}',  # Formatea el número a 3 dígitos
        'estado': numero[1],
        'comprador': numero[2] if numero[2] else "",  # Si el comprador es vacío, mostrar vacío
        'pagado': numero[3]
    } for numero in numeros]

    return render_template("numeros.html", numeros=numeros_formateados)

# Marca un número como vendido o pagado
@app.route("/actualizar", methods=["POST"])
def actualizar_numero():
    numero = request.form["numero"]
    comprador = request.form.get("comprador", "Anónimo")
    pagado = request.form.get("pagado") == 'true'

    conn = sqlite3.connect("rifa.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE rifas
        SET comprador = ?, pagado = ?
        WHERE numero = ? AND estado = 'vendido'
    """, (comprador, pagado, numero))
    conn.commit()
    conn.close()

    return jsonify({"message": f"El número {numero} ha sido actualizado."}), 200

if __name__ == "__main__":
    app.run(debug=True)