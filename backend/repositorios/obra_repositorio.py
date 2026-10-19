import mysql.connector
from config import DB_CONFIG
from modelos.obra import Obra


class ObraRepositorio:
    def listar_activas(self):
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM obras WHERE activa = TRUE")
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        # Cada fila de la tabla se convierte en un objeto Obra
        return [Obra(**fila) for fila in filas]