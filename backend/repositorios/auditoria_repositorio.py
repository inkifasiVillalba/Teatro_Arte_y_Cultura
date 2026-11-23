import mysql.connector
from config import DB_CONFIG


class AuditoriaRepositorio:
    def __conectar(self):
        return mysql.connector.connect(**DB_CONFIG)

    def registrar(self, accion, detalle, id_usuario=None):
        conexion = self.__conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO registro_operacion (accion, detalle, id_usuario) "
            "VALUES (%s, %s, %s)",
            (accion, detalle, id_usuario),
        )
        conexion.commit()
        cursor.close()
        conexion.close()

    def listar(self, limite=100):
        conexion = self.__conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT r.id, r.fecha, r.accion, r.detalle, u.nombre AS usuario "
            "FROM registro_operacion r "
            "LEFT JOIN usuarios u ON u.id = r.id_usuario "
            "ORDER BY r.fecha DESC, r.id DESC LIMIT %s",
            (limite,),
        )
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return filas