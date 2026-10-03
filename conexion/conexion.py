import pymysql

def obtener_conexion():
    conexion = pymysql.connect(
        host='localhost',
        user='root',
        password='',        # <-- Déjalo vacío
        database='indec'    # <-- O el nombre de tu base de datos
    )
    return conexion