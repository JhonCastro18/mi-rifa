# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 14:21:12 2025

@author: karen
"""

import sqlite3

# Conectamos con la base de datos (o la creamos si no existe)
conn = sqlite3.connect("rifa.db")
cursor = conn.cursor()

# Creamos una tabla para guardar los números de la rifa
cursor.execute("""
CREATE TABLE IF NOT EXISTS rifas (
    numero INTEGER PRIMARY KEY,
    estado TEXT DEFAULT 'disponible',
    comprador TEXT
)
""")

# Agregamos los números del 000 al 999 a la tabla
cursor.execute("DELETE FROM rifas")  # Limpiamos por si ya hay datos
for i in range(1000):
    cursor.execute("INSERT INTO rifas (numero) VALUES (?)", (i,))

# Guardamos los cambios y cerramos
conn.commit()
conn.close()

print("Base de datos creada con éxito.")