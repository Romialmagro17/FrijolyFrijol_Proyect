from flask_login import UserMixin
from conexion.conexion import obtener_conexion

class User(UserMixin):
    def __init__(self, id, usuario):
        self.id = str(id)
        self.usuario = usuario

def load_user(user_id):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id, usuario FROM usuarios WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conexion.close()
        if user_data:
            return User(user_data['id'], user_data['usuario'])
    return None