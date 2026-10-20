import mysql.connector
from config import DB_CONFIG


class FuncionRepositorio:
    def __conectar(self):
        return mysql.connector.connect(**DB_CONFIG)

    def listar_por_obra(self, id_obra):
        conexion = self.__conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT f.id, f.fecha_hora, f.precio, s.nombre AS sala, s.capacidad "
            "FROM funciones f JOIN salas s ON f.id_sala = s.id "
                        "WHERE f.id_obra = %s AND f.estado = 'PROGRAMADA' AND f.fecha_hora >= NOW() "
            "ORDER BY f.fecha_hora",
            (id_obra,),
        )
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return filas

    def listar_asientos(self, id_funcion):
        """Todos los asientos de la sala, marcando cuáles están ocupados."""
        conexion = self.__conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT a.id, a.fila, a.numero, "
            "  (SELECT COUNT(*) FROM entradas e "
            "   WHERE e.id_funcion = f.id AND e.id_asiento = a.id "
            "   AND e.estado <> 'ANULADA') AS vendido, "
            "  (SELECT COUNT(*) FROM detalle_reserva d "
            "   JOIN reservas r ON d.id_reserva = r.id "
            "   WHERE r.id_funcion = f.id AND d.id_asiento = a.id "
            "   AND r.estado = 'PENDIENTE') AS reservado "
            "FROM funciones f JOIN asientos a ON a.id_sala = f.id_sala "
            "WHERE f.id = %s ORDER BY a.fila, a.numero",
            (id_funcion,),
        )
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return [
            {
                "id": f["id"],
                "codigo": f"{f['fila']}-{f['numero']}",
                "fila": f["fila"],
                "ocupado": (f["vendido"] + f["reservado"]) > 0,
            }
            for f in filas
        ]


    def listar_todas(self):
        conexion = self.__conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT f.id, f.fecha_hora, f.precio, f.estado, "
            " o.titulo, o.duracion_min, s.nombre AS sala, s.capacidad, "
            " (SELECT COUNT(*) FROM entradas e WHERE e.id_funcion = f.id "
            "  AND e.estado <> 'ANULADA') AS vendidas "
            "FROM funciones f "
            "JOIN obras o ON f.id_obra = o.id "
            "JOIN salas s ON f.id_sala = s.id "
            "ORDER BY f.fecha_hora"
        )
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return filas

    def listar_de_sala(self, id_sala):
        """Funciones activas de una sala, con la duración de su obra."""
        conexion = self.__conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT f.id, f.fecha_hora, f.precio, o.titulo, o.duracion_min "
            "FROM funciones f JOIN obras o ON f.id_obra = o.id "
            "WHERE f.id_sala = %s AND f.estado <> 'CANCELADA'",
            (id_sala,),
        )
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return filas

    def crear(self, id_obra, id_sala, fecha_hora, precio):
        conexion = self.__conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO funciones (id_obra, id_sala, fecha_hora, precio) "
            "VALUES (%s, %s, %s, %s)",
            (id_obra, id_sala, fecha_hora, precio),
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        conexion.close()
        return nuevo_id