import mysql.connector
from config import DB_CONFIG


class EntradaRepositorio:
    def __conectar(self):
        return mysql.connector.connect(**DB_CONFIG)

    def buscar_por_codigo(self, codigo):
        conexion = self.__conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM entradas WHERE codigo = %s", (codigo,))
        fila = cursor.fetchone()
        cursor.close()
        conexion.close()
        return fila

    def actualizar_estado(self, id_entrada, estado):
        conexion = self.__conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE entradas SET estado = %s WHERE id = %s",
            (estado, id_entrada),
        )
        conexion.commit()
        cursor.close()
        conexion.close()