from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración de la base de datos (se creará un archivo llamado ideas.db)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'ideas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de la base de datos
class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)

# Crear la base de datos automáticamente
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        nuevo_nombre = request.form.get('nombre')
        nueva_categoria = request.form.get('categoria')
        
        # Guardar en la base de datos
        nueva_idea = Idea(nombre=nuevo_nombre, categoria=nueva_categoria)
        db.session.add(nueva_idea)
        db.session.commit()
        return redirect(url_for('home'))

    # Leer todas las ideas de la base de datos
    todas_las_ideas = Idea.query.all()
    return render_template('index.html', ideas=todas_las_ideas)

if __name__ == '__main__':
    app.run(debug=True, port=8080)