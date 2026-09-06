import os
import sqlite3
from flask import Flask, render_template, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_para_csrf_12345'

# --- CONFIGURACIÓN DE LA BASE DE DATOS SQLITE ---
DATA_FOLDER = os.path.join(app.root_path, 'data')
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

DB_PATH = os.path.join(DATA_FOLDER, 'ferreteria.db')

def dict_factory(cursor, row):
    """Convierte las filas de SQLite en diccionarios para usar notación de punto en Jinja2."""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def init_db():
    """Inicializa la base de datos y crea la tabla de productos si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            descripcion TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Ejecutar la inicialización de la base de datos al arrancar la app
init_db()

# Listas temporales restantes
CLIENTES = []
PROVEEDORES = []
FACTURAS = []

# --- RUTA PRINCIPAL ---
@app.route('/')
def index():
    return render_template('index.html')

# --- MÓDULO PRODUCTOS (Con persistencia SQLite) ---
@app.route('/productos')
def productos():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, precio, stock, descripcion FROM productos')
    productos_db = cursor.fetchall()
    conn.close()
    return render_template('productos.html', productos=productos_db)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def formulario_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        precio = float(form.precio.data) if form.precio.data is not None else 0.0
        stock = int(form.stock.data) if form.stock.data is not None else 0
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, precio, stock, descripcion)
            VALUES (?, ?, ?, ?)
        ''', (nombre, precio, stock, 'Sin descripción'))
        conn.commit()
        conn.close()
        
        flash('Producto guardado exitosamente', 'success')
        return redirect(url_for('productos'))
    return render_template('formulario_producto.html', form=form)

# --- MÓDULO CLIENTES ---
@app.route('/clientes')
def clientes():
    return render_template('clientes.html', clientes=CLIENTES)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def formulario_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        CLIENTES.append(form.data)
        flash('Cliente registrado exitosamente', 'success')
        return redirect(url_for('clientes'))
    return render_template('formulario_cliente.html', form=form)

# --- MÓDULO PROVEEDORES ---
@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html', proveedores=PROVEEDORES)

@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def formulario_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        PROVEEDORES.append(form.data)
        flash('Proveedor guardado exitosamente', 'success')
        return redirect(url_for('proveedores'))
    return render_template('formulario_proveedor.html', form=form)

# --- MÓDULO FACTURACIÓN ---
@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html', facturas=FACTURAS)

@app.route('/facturacion/nueva', methods=['GET', 'POST'])
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