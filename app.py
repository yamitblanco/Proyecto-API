from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime  # Asegúrate de tener esta importación arriba del todo
import sqlite3

# Inicialización de la aplicación Flask
app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura'  # Clave secreta para gestionar sesiones y mensajes flash


# Función para conectar a la base de datos
def connect_db():
    conn = sqlite3.connect('stock_plus.db')  # Conexión a la base de datos
    return conn


# Ruta raíz: Página de inicio
@app.route('/')
def index():
    return render_template('inicio.html')  # Renderiza la página de inicio


# Ruta para iniciar sesión
@app.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':  # Si la solicitud es POST, significa que el usuario ha enviado el formulario
        email = request.form['email']
        contraseña = request.form['contraseña']

        # Conexión a la base de datos para validar el inicio de sesión
        conn = sqlite3.connect('stock_plus.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ? AND contraseña = ?', (email, contraseña))
        usuario = cursor.fetchone()  # Recupera el usuario si las credenciales son correctas
        conn.close()

        if usuario:
            session['usuario_id'] = usuario[0]
            session['usuario_nombre'] = usuario[1]
            session['usuario_fecha'] = datetime.now().strftime('%Y-%m-%d')  # Guardamos fecha actual
            session['usuario_hora'] = datetime.now().strftime('%H:%M:%S')  # Guardamos hora actual
            session['usuario_rol'] = 'Gestor de Inventarios'  # Rol fijo por ahora
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('bienvenido'))

        flash('Credenciales incorrectas. Intenta de nuevo.', 'error')  # Mensaje de error
        return redirect(url_for('inicio'))  # Redirige a la página de inicio de sesión si las credenciales son incorrectas

    return render_template('inicio.html')  # Renderiza el formulario de inicio de sesión


# Ruta para consultar productos por fecha
@app.route('/buscar_productos', methods=['POST'])
def buscar_productos():
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']

    # Consulta a la base de datos para obtener productos entre las fechas especificadas
    conn = sqlite3.connect('stock_plus.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT nombre_producto, estado, ubicacion, cantidad, precio, fecha_registro
        FROM productos
        WHERE DATE(fecha_registro) BETWEEN ? AND ?
        ORDER BY DATE(fecha_registro) ASC
    ''', (fecha_inicio, fecha_fin))
    productos = cursor.fetchall()  # Recupera todos los productos que coinciden con el rango de fechas
    conn.close()

    return render_template('consulta_productos.html', productos=productos, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)


# Ruta para editar un producto
@app.route('/editar_producto', methods=['GET', 'POST'])
def editar_producto():
    conn = sqlite3.connect('stock_plus.db')
    cursor = conn.cursor()

    if request.method == 'GET':  # Si el método es GET, obtenemos los datos del producto para editarlo
        nombre_producto = request.args.get('nombre_producto')
        cursor.execute('SELECT * FROM productos WHERE nombre_producto = ?', (nombre_producto,))
        producto = cursor.fetchone()
        conn.close()
        return render_template('editar_producto.html', producto=producto)

    elif request.method == 'POST':  # Si el método es POST, actualizamos los datos del producto
        id_producto = request.form['id_producto']
        nombre = request.form['nombre_producto']
        estado = request.form['estado']
        ubicacion = request.form['ubicacion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        cursor.execute('''
            UPDATE productos 
            SET nombre_producto = ?, estado = ?, ubicacion = ?, cantidad = ?, precio = ?
            WHERE id_producto = ?
        ''', (nombre, estado, ubicacion, cantidad, precio, id_producto))
        conn.commit()
        conn.close()
        flash('Producto actualizado correctamente.')  # Mensaje de éxito
        return redirect(url_for('informes'))  # Redirige a la página de informes


# Ruta para eliminar un producto
@app.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    nombre_producto = request.form['nombre_producto']

    conn = sqlite3.connect('stock_plus.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE nombre_producto = ?', (nombre_producto,))
    conn.commit()
    conn.close()

    flash('Producto eliminado con éxito.')  # Mensaje de éxito
    return redirect(url_for('informes'))  # Redirige a la página de informes


# Ruta para registrar un nuevo usuario
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':  # Si el método es POST, intentamos registrar al nuevo usuario
        nombres = request.form['nombres']
        primer_apellido = request.form['primer_apellido']
        segundo_apellido = request.form['segundo_apellido']
        fecha_nacimiento = request.form['fecha_nacimiento']
        telefono = request.form['telefono']
        email = request.form['email']
        contraseña = request.form['contraseña']

        conn = sqlite3.connect('stock_plus.db')
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO usuarios (nombres, primer_apellido, segundo_apellido, fecha_nacimiento, telefono, email, contraseña) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                           (nombres, primer_apellido, segundo_apellido, fecha_nacimiento, telefono, email, contraseña))
            conn.commit()
            flash('Registro exitoso. Ahora inicia sesión.')
            return redirect(url_for('inicio'))
        except sqlite3.IntegrityError:  # Si el email ya está registrado
            flash('El email ya está registrado.')
            return redirect(url_for('registro'))
        finally:
            conn.close()

    return render_template('registro.html')  # Renderiza la página de registro


# Ruta para registrar un producto
@app.route('/registro_productos', methods=['GET', 'POST'])
def registro_productos():
    if request.method == 'POST':  # Si el método es POST, intentamos registrar un nuevo producto
        nombre_producto = request.form['nombre_producto']
        estado = request.form['estado']
        ubicacion = request.form['ubicacion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        fecha_registro = request.form['fecha_registro']

        conn = sqlite3.connect('stock_plus.db')
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO productos (nombre_producto, estado, ubicacion, cantidad, precio) VALUES (?, ?, ?, ?, ?)', 
                           (nombre_producto, estado, ubicacion, cantidad, precio))
            conn.commit()
            flash('Registro producto exitoso.', 'success')  # Mensaje de éxito
            return redirect(url_for('bienvenido'))
        except sqlite3.IntegrityError:  # Si el producto ya está registrado
            flash('Producto ya registrado, ¿deseas modificarlo?')
            return redirect(url_for('bienvenido'))
        finally:
            conn.close()

    return render_template('bienvenido.html')  # Renderiza la página de bienvenida


# Ruta de bienvenida después de iniciar sesión
@app.route('/bienvenido')
def bienvenido():
    return render_template('bienvenido.html')


# Ruta para ver informes
@app.route('/informes')
def informes():
    return render_template('informes.html')


# Ruta para contacto sin registrar
@app.route('/contactonoreg', methods=['GET', 'POST'])
def contactonoreg():
    if request.method == 'POST':
        return redirect(url_for('contact_submit'))
    return render_template('contactonoreg.html')


# Ruta para contacto con usuario registrado
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        return redirect(url_for('contact_submit'))
    return render_template('contacto.html')


# Simulación de envío de mensaje de contacto
@app.route('/contact_submit')
def contact_submit():
    return "<h1>Gracias por tu mensaje. Te responderemos pronto.</h1><a href='/'>Volver</a>"


# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
