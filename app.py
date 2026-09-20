import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import obtener_conexion
from models import User, load_user
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.usuario_form import UsuarioForm
from forms.login_form import LoginForm

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_para_csrf_12345'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user_callback(user_id):
    return load_user(user_id)

# Listas temporales para los módulos que aún no usan BD relacional
IDEAS = []
CLIENTES = []
PROVEEDORES = []
FACTURAS = []

# --- RUTA PRINCIPAL (REGISTRO DE IDEAS) ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre_idea = request.form.get('nombre')
        categoria = request.form.get('categoria')
        if nombre_idea:
            IDEAS.append({'nombre': nombre_idea, 'categoria': categoria})
            flash('Idea registrada exitosamente', 'success')
        return redirect(url_for('index'))
    return render_template('index.html', ideas=IDEAS)

# --- RUTAS DE AUTENTICACIÓN ---
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = UsuarioForm()
    if form.validate_on_submit():
        usuario = form.usuario.data
        password_plana = form.password.data
        
        # Generar hash seguro de la contraseña
        password_hash = generate_password_hash(password_plana)
        
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "INSERT INTO usuarios (usuario, password) VALUES (%s, %s)",
                    (usuario, password_hash)
                )
                conexion.commit()
                cursor.close()
                conexion.close()
                flash('Usuario registrado exitosamente. Ahora puedes iniciar sesión.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                flash('El nombre de usuario ya existe o ocurrió un error.', 'danger')
    return render_template('registro.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        usuario_ingresado = form.usuario.data
        password_ingresada = form.password.data
        
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id, usuario, password FROM usuarios WHERE usuario = %s", (usuario_ingresado,))
            user_data = cursor.fetchone()
            cursor.close()
            conexion.close()
            
            if user_data and check_password_hash(user_data['password'], password_ingresada):
                user_obj = User(user_data['id'], user_data['usuario'])
                login_user(user_obj)
                flash('Has iniciado sesión correctamente.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('login'))

# --- MÓDULO PRODUCTOS (Protegidos con @login_required) ---
@app.route('/productos')
@login_required
def productos():
    conexion = obtener_conexion()
    productos_db = []
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute('SELECT id, nombre, precio, stock, descripcion FROM productos')
        productos_db = cursor.fetchall()
        cursor.close()
        conexion.close()
    return render_template('productos.html', productos=productos_db)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def formulario_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        precio = float(form.precio.data) if form.precio.data is not None else 0.0
        stock = int(form.stock.data) if form.stock.data is not None else 0
        
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute(
                """
                INSERT INTO productos (nombre, precio, stock, descripcion)
                VALUES (%s, %s, %s, %s)
                """,
                (nombre, precio, stock, 'Sin descripción')
            )
            conexion.commit()
            cursor.close()
            conexion.close()
            
            flash('Producto guardado exitosamente', 'success')
            return redirect(url_for('productos'))
    return render_template('formulario_producto.html', form=form)

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    if request.method == 'POST':
        form = ProductoForm()
        if form.validate_on_submit():
            nombre = form.nombre.data
            precio = float(form.precio.data) if form.precio.data is not None else 0.0
            stock = int(form.stock.data) if form.stock.data is not None else 0
            
            cursor.execute(
                """
                UPDATE productos SET nombre = %s, precio = %s, stock = %s WHERE id = %s
                """,
                (nombre, precio, stock, id)
            )
            conexion.commit()
            cursor.close()
            conexion.close()
            flash('Producto actualizado exitosamente', 'success')
            return redirect(url_for('productos'))
    else:
        cursor.execute('SELECT id, nombre, precio, stock FROM productos WHERE id = %s', (id,))
        producto = cursor.fetchone()
        form = ProductoForm(data=producto)
        cursor.close()
        conexion.close()
        return render_template('formulario_producto.html', form=form)

@app.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM productos WHERE id = %s', (id,))
        conexion.commit()
        cursor.close()
        conexion.close()
        flash('Producto eliminado exitosamente', 'success')
    return redirect(url_for('productos'))

# --- MÓDULO CLIENTES ---
@app.route('/clientes')
@login_required
def clientes():
    return render_template('clientes.html', clientes=CLIENTES)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
@login_required
def formulario_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        CLIENTES.append(form.data)
        flash('Cliente registrado exitosamente', 'success')
        return redirect(url_for('clientes'))
    return render_template('formulario_cliente.html', form=form)

# --- MÓDULO PROVEEDORES ---
@app.route('/proveedores')
@login_required
def proveedores():
    return render_template('proveedores.html', proveedores=PROVEEDORES)

@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
@login_required
def formulario_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        PROVEEDORES.append(form.data)
        flash('Proveedor guardado exitosamente', 'success')
        return redirect(url_for('proveedores'))
    return render_template('formulario_proveedor.html', form=form)

# --- MÓDULO FACTURACIÓN ---
@app.route('/facturacion')
@login_required
def facturacion():
    return render_template('facturacion.html', facturas=FACTURAS)

@app.route('/facturacion/nueva', methods=['GET', 'POST'])
@login_required
def formulario_facturacion():
    form = FacturacionForm()
    if form.validate_on_submit():
        FACTURAS.append(form.data)
        flash('Factura generada exitosamente', 'success')
        return redirect(url_for('facturacion'))
    return render_template('formulario_facturacion.html', form=form)

# --- EJECUCIÓN DEL SERVIDOR ---
if __name__ == '__main__':
    app.run(debug=True)