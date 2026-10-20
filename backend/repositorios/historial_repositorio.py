import mysql.connector
from config import DB_CONFIG


class HistorialRepositorio:
    def entradas_de_cliente(self, id_cliente):
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT e.codigo, e.estado, e.precio, o.titulo, f.fecha_hora, "
            " CONCAT(a.fila, '-', a.numero) AS asiento, s.nombre AS sala "
            "FROM entradas e "
            "JOIN ventas v ON e.id_venta = v.id "
            "JOIN funciones f ON e.id_funcion = f.id "
            "JOIN obras o ON f.id_obra = o.id "
            "JOIN salas s ON f.id_sala = s.id "
            "JOIN asientos a ON e.id_asiento = a.id "
            "WHERE v.id_cliente = %s ORDER BY f.fecha_hora DESC",
            (id_cliente,),
        )
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return filas

    def reservas_de_cliente(self, id_cliente):
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT r.id, r.estado, o.titulo, f.fecha_hora, "
            " GROUP_CONCAT(CONCAT(a.fila, '-', a.numero) SEPARATOR ', ') AS asientos, "
            " SUM(d.precio) AS total "
            "FROM reservas r "
            "JOIN funciones f ON r.id_funcion = f.id "
            "JOIN obras o ON f.id_obra = o.id "
            "JOIN detalle_reserva d ON d.id_reserva = r.id "
            "JOIN asientos a ON d.id_asiento = a.id "
            "WHERE r.id_cliente = %s "
            "GROUP BY r.id, r.estado, o.titulo, f.fecha_hora "
            "ORDER BY r.id DESC",
            (id_cliente,),
        )
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return filas