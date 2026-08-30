from flask import Flask, render_template, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_para_csrf_12345'

# Listas temporales en memoria
PRODUCTOS = []
CLIENTES = []
PROVEEDORES = []
FACTURAS = []

# --- RUTA PRINCIPAL ---
@app.route('/')
def index():
    return render_template('index.html')

# --- MÓDULO PRODUCTOS ---
@app.route('/productos')
def productos():
    return render_template('productos.html', productos=PRODUCTOS)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def formulario_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        PRODUCTOS.append(form.data)
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