import os
from flask import Flask, render_template, redirect, url_for, flash, request
from conexion.conexion import obtener_conexion
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_para_csrf_12345'

# Listas temporales
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

# --- MÓDULO PRODUCTOS (CRUD Completo en Base de Datos) ---
@app.route('/productos')
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