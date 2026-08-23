import sqlite3
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


# Función para conectar a la base de datos de ideas
def init_sqlite_db():
  conn = sqlite3.connect('ideas.db')
  conn.execute(
      'CREATE TABLE IF NOT EXISTS ideas (id INTEGER PRIMARY KEY AUTOINCREMENT,'
      ' nombre TEXT, categoria TEXT)'
  )
  conn.close()


init_sqlite_db()


@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    nombre = request.form['nombre']
    categoria = request.form['categoria']

    conn = sqlite3.connect('ideas.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO ideas (nombre, categoria) VALUES (?, ?)',
        (nombre, categoria),
    )
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

  # Consultar ideas de la base de datos
  conn = sqlite3.connect('ideas.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM ideas')
  ideas = cursor.fetchall()
  conn.close()

  return render_template('index.html', ideas=ideas)


@app.route('/productos')
def productos():
  # Merchandising oficial de Frijol y Frijol
  lista_productos = [
      {'nombre': 'Camiseta Adulto Frijol y Frijol', 'precio': 15.00, 'stock': 20},
      {'nombre': 'Camiseta Niño Frijol y Frijol', 'precio': 12.00, 'stock': 15},
      {'nombre': 'Gorra Frijol y Frijol', 'precio': 9.50, 'stock': 8},
      {
          'nombre': 'Mochila Escolar Frijol y Frijol',
          'precio': 25.00,
          'stock': 0,
      },
  ]
  return render_template('productos.html', productos=lista_productos)


@app.route('/clientes')
def clientes():
  seguidores = [
      {
          'nombre': 'Carla Gómez',
          'comentario': '¡Me encantan sus vlogs en familia!',
          'vip': True,
      },
      {'nombre': 'Mateo Pérez', 'comentario': 'Saludos desde Quito', 'vip': False},
      {
          'nombre': 'Sofía Ruiz',
          'comentario': 'El unboxing estuvo genial',
          'vip': True,
      },
  ]
  return render_template('clientes.html', clientes=seguidores)


@app.route('/proveedores')
def proveedores():
  # Proveedores reales solicitados
  aliados = [
      {
          'empresa': 'Mi Juguetería',
          'pais': 'Ecuador',
          'contacto': 'ventas@mijugueteria.ec',
          'activo': True,
      },
      {
          'empresa': 'Juguetón',
          'pais': 'Ecuador',
          'contacto': 'contacto@jugueton.com.ec',
          'activo': True,
      },
  ]
  return render_template('proveedores.html', proveedores=aliados)


@app.route('/facturacion')
def facturacion():
  pedidos = [
      {
          'id_pedido': 'F-001',
          'item': 'Camiseta Adulto Frijol y Frijol',
          'total': 15.00,
      },
      {'id_pedido': 'F-002', 'item': 'Gorra Frijol y Frijol', 'total': 9.50},
  ]
  return render_template('facturacion.html', pedidos=pedidos)


if __name__ == '__main__':
  app.run(debug=True)