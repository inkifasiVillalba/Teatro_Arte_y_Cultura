import mysql.connector
from config import DB_CONFIG


class DashboardRepositorio:
    def __conectar(self):
        return mysql.connector.connect(**DB_CONFIG)

    def indicadores(self):
        """Totales de ventas, boletas, funciones activas y unidades de cafetería."""
        conexion = self.__conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT COALESCE(SUM(total), 0) AS total, COUNT(*) AS n FROM ventas")
        ventas = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) AS n FROM entradas WHERE estado <> 'ANULADA'")
        boletas = cursor.fetchone()["n"]
        cursor.execute(
            "SELECT COUNT(*) AS n FROM funciones WHERE estado = 'PROGRAMADA' AND fecha_hora >= NOW()"
        )
        funciones = cursor.fetchone()["n"]
        cursor.execute("SELECT COALESCE(SUM(cantidad), 0) AS n FROM detalle_venta_producto")
        cafeteria = cursor.fetchone()["n"]
        cursor.close()
        conexion.close()
        return {
            "ventas_totales": float(ventas["total"]),
            "transacciones": ventas["n"],
            "boletas": boletas,
            "funciones_activas": funciones,
            "cafeteria_uds": int(cafeteria),
        }

    def ocupacion_por_sala(self):
        """Asientos vendidos frente a la capacidad de las funciones programadas de cada sala."""
        conexion = self.__conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT s.id, s.nombre, s.capacidad, COUNT(DISTINCT f.id) AS funciones, "
            " COALESCE(SUM(v.n), 0) AS vendidos "
            "FROM salas s "
            "LEFT JOIN funciones f ON f.id_sala = s.id AND f.estado = 'PROGRAMADA' AND f.fecha_hora >= NOW() "
            "LEFT JOIN (SELECT id_funcion, COUNT(*) AS n FROM entradas "
            "           WHERE estado <> 'ANULADA' GROUP BY id_funcion) v ON v.id_funcion = f.id "
            "GROUP BY s.id, s.nombre, s.capacidad ORDER BY s.id"
        )
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return filas
