# -*- coding: utf-8 -*-
import sqlite3

# Conectar a la base de datos (si no existe, se creará)
conn = sqlite3.connect('rifa.db')

# Crear un cursor
cursor = conn.cursor()

# Asegurarse de que la tabla existe y limpiarla
cursor.execute("DROP TABLE IF EXISTS rifas")  # Limpiar tabla existente
cursor.execute('''
CREATE TABLE IF NOT EXISTS rifas (
    numero TEXT PRIMARY KEY,
    estado TEXT DEFAULT 'disponible',
    comprador TEXT,
    pagado BOOLEAN DEFAULT FALSE
)
''')

# Insertar los números del 000 al 999 en la tabla
for i in range(1000):
    numero = f'{i:03}'  # Asegura que el número tenga tres dígitos
    # Usamos INSERT OR IGNORE para evitar duplicados si ya existen
    cursor.execute("INSERT OR IGNORE INTO rifas (numero, estado, comprador, pagado) VALUES (?, 'disponible', '', 0)", (numero,))

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos y tabla creadas correctamente.")