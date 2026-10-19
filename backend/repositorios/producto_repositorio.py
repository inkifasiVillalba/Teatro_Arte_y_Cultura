import mysql.connector
from config import DB_CONFIG


class ProductoRepositorio:
    def __conectar(self):
        return mysql.connector.connect(**DB_CONFIG)

    def listar_activos(self):
        conexion = self.__conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE activo = TRUE")
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return filas

    def buscar_por_id(self, id_producto):
        conexion = self.__conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id = %s", (id_producto,))
        fila = cursor.fetchone()
        cursor.close()
        conexion.close()
        return fila

    def actualizar_existencias(self, id_producto, existencias):
        conexion = self.__conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE productos SET existencias = %s WHERE id = %s",
            (existencias, id_producto),
        )
        conexion.commit()
        cursor.close()
        conexion.close()