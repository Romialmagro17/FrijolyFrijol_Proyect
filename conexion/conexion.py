import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="tu_password", # Cambia por tu contraseña de MySQL
            database="nombre_de_tu_base" # Cambia por el nombre de tu base de datos
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return None