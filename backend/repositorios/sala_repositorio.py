import mysql.connector
from config import DB_CONFIG
from modelos.sala import Sala


class SalaRepositorio:
    def listar(self):
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM salas ORDER BY id")
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return [Sala(**fila) for fila in filas]

    def buscar_por_id(self, id_sala):
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM salas WHERE id = %s", (id_sala,))
        fila = cursor.fetchone()
        cursor.close()
        conexion.close()
        return Sala(**fila) if fila else None