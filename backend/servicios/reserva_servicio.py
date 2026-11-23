from repositorios.reserva_repositorio import ReservaRepositorio
from servicios.auditoria_servicio import AuditoriaServicio


class ReservaServicio:
    def __init__(self):
        self.__repo = ReservaRepositorio()
        self.__auditoria = AuditoriaServicio()

    def reservar(self, id_cliente, id_funcion, asientos, precio):
        if not asientos:
            raise ValueError("Debes elegir al menos un asiento")
        resultado = self.__repo.crear(id_cliente, id_funcion, asientos, precio)
        self.__auditoria.registrar(
            "RESERVAR_ASIENTOS",
            f"{len(asientos)} asiento(s) reservado(s) en la función #{id_funcion}",
            id_cliente,
        )
        return resultado

    def pendientes(self):
        filas = self.__repo.listar_pendientes()
        for f in filas:
            f["fecha_hora"] = f["fecha_hora"].strftime("%Y-%m-%d %H:%M")
            f["total"] = float(f["total"])
        return filas

    def cobrar(self, id_reserva, id_empleado, metodo):
        if metodo not in ("EFECTIVO", "TARJETA", "TRANSFERENCIA"):
            raise ValueError("Método de pago no válido")
        resultado = self.__repo.cobrar(id_reserva, id_empleado, metodo)
        self.__auditoria.registrar(
            "COBRAR_RESERVA",
            f"Reserva #{id_reserva} cobrada ({metodo})",
            id_empleado,
        )
        return resultado

    def cancelar(self, id_reserva):
        self.__repo.cancelar(id_reserva)