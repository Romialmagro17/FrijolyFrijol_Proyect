from flask_login import UserMixin
from conexion.conexion import obtener_conexion

class User(UserMixin):
    def __init__(self, id, usuario):
        self.id = str(id)
        self.usuario = usuario

def load_user(user_id):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, usuario FROM usuarios WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conexion.close()
        if row:
            return User(row[0], row[1]) # <-- row[0] es el id, row[1] es el usuario
    return None