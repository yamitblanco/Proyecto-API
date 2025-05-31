import sqlite3

conn = sqlite3.connect("stock_plus.db")
cursor = conn.cursor()

# Leer usuarios
cursor.execute("SELECT * FROM usuarios;")
usuarios = cursor.fetchall()
print("Usuarios:", usuarios)

# Leer productos
cursor.execute("SELECT * FROM productos;")
productos = cursor.fetchall()
print("Productos:", productos)

conn.close()
