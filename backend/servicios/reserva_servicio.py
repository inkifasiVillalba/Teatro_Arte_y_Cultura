from repositorios.reserva_repositorio import ReservaRepositorio


class ReservaServicio:
    def __init__(self):
        self.__repo = ReservaRepositorio()

    def reservar(self, id_cliente, id_funcion, asientos, precio):
        if not asientos:
            raise ValueError("Debes elegir al menos un asiento")
        return self.__repo.crear(id_cliente, id_funcion, asientos, precio)

    def pendientes(self):
        filas = self.__repo.listar_pendientes()
        for f in filas:
            f["fecha_hora"] = f["fecha_hora"].strftime("%Y-%m-%d %H:%M")
            f["total"] = float(f["total"])
        return filas

    def cobrar(self, id_reserva, id_empleado, metodo):
        if metodo not in ("EFECTIVO", "TARJETA", "TRANSFERENCIA"):
            raise ValueError("Método de pago no válido")
        return self.__repo.cobrar(id_reserva, id_empleado, metodo)

    def cancelar(self, id_reserva):
        self.__repo.cancelar(id_reserva)