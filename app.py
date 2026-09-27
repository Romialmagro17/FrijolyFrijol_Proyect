# --- MÓDULO PRODUCTOS (Con JOIN obligatorio a Proveedores) ---
@app.route('/productos')
@login_required
def productos():
    conexion = obtener_conexion()
    productos_db = []
    if conexion:
        try:
            cursor = conexion.cursor()
            # Consulta JOIN entre productos y proveedores
            cursor.execute('''
                SELECT p.id_producto, p.nombre, p.precio, p.stock, p.descripcion, pr.nombre AS proveedor_nombre
                FROM productos p
                JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
            ''')
            productos_db = cursor.fetchall()
            cursor.close()
            conexion.close()
        except Exception as e:
            flash(f'Error al cargar productos: {e}', 'danger')
    return render_template('productos.html', productos=productos_db)