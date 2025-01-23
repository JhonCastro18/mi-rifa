import os
import psycopg2
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Obtener la URL de la base de datos desde la variable de entorno
DATABASE_URL = os.getenv('DATABASE_URL')

# Función para conectar a la base de datos PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

# Muestra los números disponibles
@app.route("/")
def mostrar_numeros():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT numero, estado, comprador, pagado FROM rifas")
    numeros = cursor.fetchall()
    conn.close()

    numeros_formateados = [{
        'numero': f'{numero[0]:03}',
        'estado': numero[1],
        'comprador': numero[2] if numero[2] else "",
        'pagado': numero[3]
    } for numero in numeros]

    return render_template("numeros.html", numeros=numeros_formateados)

# Busca un número específico
@app.route("/buscar/<int:numero>")
def buscar_numero(numero):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT numero, estado, comprador, pagado FROM rifas WHERE numero = %s", (numero,))
    numero_info = cursor.fetchone()
    conn.close()

    if numero_info:
        numero_formateado = {
            'numero': f'{numero_info[0]:03}',
            'estado': numero_info[1],
            'comprador': numero_info[2] if numero_info[2] else "",
            'pagado': numero_info[3]
        }
        return render_template("numero.html", numero=numero_formateado)
    else:
        return jsonify({"message": "Número no encontrado."}), 404

# Marca un número como vendido o pagado
@app.route("/actualizar", methods=["POST"])
def actualizar_numero():
    numero = request.form["numero"]
    comprador = request.form.get("comprador", "")
    pagado = request.form.get("pagado", 'false').lower() == 'true'

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT estado, comprador FROM rifas WHERE numero = %s", (numero,))
    resultado = cursor.fetchone()

    if resultado:
        estado_actual = resultado[0]
        comprador_actual = resultado[1]

        if estado_actual == "vendido":
            cursor.execute("UPDATE rifas SET pagado = %s WHERE numero = %s", (pagado, numero))
        elif estado_actual == "disponible":
            cursor.execute("""
                UPDATE rifas
                SET comprador = %s, pagado = %s, estado = 'vendido'
                WHERE numero = %s
            """, (comprador or "Anónimo", pagado, numero))
        else:
            conn.close()
            return jsonify({"message": "El número no se puede actualizar."}), 400
    else:
        conn.close()
        return jsonify({"message": "Número no encontrado en la base de datos."}), 404

    conn.commit()
    conn.close()

    return jsonify({"message": f"El número {numero} ha sido actualizado."}), 200

if __name__ == "__main__":
    app.run(debug=True)