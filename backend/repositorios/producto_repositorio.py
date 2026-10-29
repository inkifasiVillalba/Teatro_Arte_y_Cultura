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

    def registrar_venta(self, id_producto, cantidad, precio_unitario, id_empleado=None, metodo="EFECTIVO"):
        """Descuenta el stock (nunca negativo) y guarda venta, detalle y pago en UNA transacción."""
        conexion = self.__conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "UPDATE productos SET existencias = existencias - %s "
                "WHERE id = %s AND existencias >= %s",
                (cantidad, id_producto, cantidad),
            )
            if cursor.rowcount == 0:
                raise ValueError("No hay suficiente stock")
            total = precio_unitario * cantidad
            cursor.execute(
                "INSERT INTO ventas (id_empleado, total) VALUES (%s, %s)",
                (id_empleado, total),
            )
            id_venta = cursor.lastrowid
            cursor.execute(
                "INSERT INTO detalle_venta_producto (id_venta, id_producto, cantidad, precio_unitario) "
                "VALUES (%s, %s, %s, %s)",
                (id_venta, id_producto, cantidad, precio_unitario),
            )
            cursor.execute(
                "INSERT INTO pagos (id_venta, monto, metodo, estado) VALUES (%s, %s, %s, 'APROBADO')",
                (id_venta, total, metodo),
            )
            conexion.commit()
            return id_venta
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()
