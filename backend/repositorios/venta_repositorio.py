import mysql.connector
from config import DB_CONFIG


class VentaRepositorio:
    def guardar_compra(self, id_cliente, id_funcion, asientos, precio, metodo,id_empleado=None):
        """Guarda venta, entradas y pago en una sola transacción."""
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        try:
            total = precio * len(asientos)
            cursor.execute(
                "INSERT INTO ventas (id_cliente, id_empleado, total) VALUES (%s, %s, %s)",
                (id_cliente, id_empleado, total),
            )
            id_venta = cursor.lastrowid

            codigos = []
            for id_asiento in asientos:
                codigo = f"TAC-{id_funcion}-{id_venta}-{id_asiento}"
                # UNIQUE (id_funcion, id_asiento) impide vender el mismo asiento dos veces
                cursor.execute(
                    "INSERT INTO entradas (id_venta, id_funcion, id_asiento, codigo, precio) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (id_venta, id_funcion, id_asiento, codigo, precio),
                )
                codigos.append(codigo)

            cursor.execute(
                "INSERT INTO pagos (id_venta, monto, metodo, estado) "
                "VALUES (%s, %s, %s, 'APROBADO')",
                (id_venta, total, metodo),
            )
            conexion.commit()
            return {"id_venta": id_venta, "total": total, "codigos": codigos}
        except mysql.connector.IntegrityError:
            conexion.rollback()
            raise ValueError("Uno de los asientos ya fue vendido")
        finally:
            cursor.close()
            conexion.close()