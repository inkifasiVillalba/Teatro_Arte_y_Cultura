import mysql.connector
from config import DB_CONFIG


class ReservaRepositorio:
    def __conectar(self):
        return mysql.connector.connect(**DB_CONFIG)

    def crear(self, id_cliente, id_funcion, asientos, precio):
        conexion = self.__conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT precio FROM funciones WHERE id = %s", (id_funcion,))
            fila = cursor.fetchone()
            if fila is None:
                raise ValueError("Función inexistente")
            precio = float(fila[0])   # el precio lo decide el servidor, no el navegador

            # Ningún asiento puede estar vendido ni reservado
            for id_asiento in asientos:
                cursor.execute(
                    "SELECT "
                    " (SELECT COUNT(*) FROM entradas WHERE id_funcion = %s "
                    "  AND id_asiento = %s AND estado <> 'ANULADA') + "
                    " (SELECT COUNT(*) FROM detalle_reserva d "
                    "  JOIN reservas r ON d.id_reserva = r.id "
                    "  WHERE r.id_funcion = %s AND d.id_asiento = %s "
                    "  AND r.estado = 'PENDIENTE')",
                    (id_funcion, id_asiento, id_funcion, id_asiento),
                )
                if cursor.fetchone()[0] > 0:
                    raise ValueError("Uno de los asientos ya está ocupado")

            cursor.execute(
                "INSERT INTO reservas (id_cliente, id_funcion) VALUES (%s, %s)",
                (id_cliente, id_funcion),
            )
            id_reserva = cursor.lastrowid
            for id_asiento in asientos:
                cursor.execute(
                    "INSERT INTO detalle_reserva (id_reserva, id_asiento, precio) "
                    "VALUES (%s, %s, %s)",
                    (id_reserva, id_asiento, precio),
                )
            conexion.commit()
            return {"id_reserva": id_reserva, "total": precio * len(asientos)}
        except ValueError:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    def listar_pendientes(self):
        conexion = self.__conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT r.id, u.nombre AS cliente, u.telefono, o.titulo, f.fecha_hora, "
            " GROUP_CONCAT(CONCAT(a.fila, '-', a.numero) SEPARATOR ', ') AS asientos, "
            " SUM(d.precio) AS total "
            "FROM reservas r "
            "JOIN usuarios u ON r.id_cliente = u.id "
            "JOIN funciones f ON r.id_funcion = f.id "
            "JOIN obras o ON f.id_obra = o.id "
            "JOIN detalle_reserva d ON d.id_reserva = r.id "
            "JOIN asientos a ON d.id_asiento = a.id "
            "WHERE r.estado = 'PENDIENTE' "
            "GROUP BY r.id, u.nombre, u.telefono, o.titulo, f.fecha_hora"
        )
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return filas

    def cobrar(self, id_reserva, id_empleado, metodo):
        """Convierte la reserva en venta + entradas + pago (una transacción)."""
        conexion = self.__conectar()
        cursor = conexion.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM reservas WHERE id = %s", (id_reserva,))
            reserva = cursor.fetchone()
            if reserva is None:
                raise ValueError("Reserva inexistente")
            if reserva["estado"] != "PENDIENTE":
                raise ValueError("Solo se puede cobrar una reserva pendiente")

            cursor.execute(
                "SELECT id_asiento, precio FROM detalle_reserva WHERE id_reserva = %s",
                (id_reserva,),
            )
            detalles = cursor.fetchall()
            total = sum(d["precio"] for d in detalles)

            cursor.execute(
                "INSERT INTO ventas (id_cliente, id_empleado, id_reserva, total) "
                "VALUES (%s, %s, %s, %s)",
                (reserva["id_cliente"], id_empleado, id_reserva, total),
            )
            id_venta = cursor.lastrowid

            codigos = []
            for d in detalles:
                codigo = f"TAC-{reserva['id_funcion']}-{id_venta}-{d['id_asiento']}"
                cursor.execute(
                    "INSERT INTO entradas (id_venta, id_funcion, id_asiento, codigo, precio) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (id_venta, reserva["id_funcion"], d["id_asiento"], codigo, d["precio"]),
                )
                codigos.append(codigo)

            cursor.execute(
                "INSERT INTO pagos (id_venta, monto, metodo, estado) "
                "VALUES (%s, %s, %s, 'APROBADO')",
                (id_venta, total, metodo),
            )
            cursor.execute(
                "UPDATE reservas SET estado = 'CONFIRMADA' WHERE id = %s", (id_reserva,)
            )
            conexion.commit()
            return {"id_venta": id_venta, "total": float(total), "codigos": codigos}
        except ValueError:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    def cancelar(self, id_reserva):
        conexion = self.__conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE reservas SET estado = 'CANCELADA' "
            "WHERE id = %s AND estado = 'PENDIENTE'",
            (id_reserva,),
        )
        afectadas = cursor.rowcount
        conexion.commit()
        cursor.close()
        conexion.close()
        if afectadas == 0:
            raise ValueError("Solo se puede cancelar una reserva pendiente")