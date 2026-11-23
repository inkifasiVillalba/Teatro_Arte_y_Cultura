from repositorios.venta_repositorio import VentaRepositorio
from servicios.auditoria_servicio import AuditoriaServicio


class VentaServicio:
    def __init__(self):
        self.__repo = VentaRepositorio()
        self.__auditoria = AuditoriaServicio()

    def comprar(self, id_cliente, id_funcion, asientos, precio, metodo, id_empleado=None):
        if not asientos:
            raise ValueError("Debes elegir al menos un asiento")
        if metodo not in ("EFECTIVO", "TARJETA", "TRANSFERENCIA"):
            raise ValueError("Método de pago no válido")

        resultado = self.__repo.guardar_compra(
            id_cliente, id_funcion, asientos, precio, metodo
        )

        accion = "VENTA_TAQUILLA" if id_empleado else "COMPRA_ONLINE"
        self.__auditoria.registrar(
            accion,
            f"{len(asientos)} entrada(s) por ${resultado['total']} ({metodo})",
            id_empleado or id_cliente,
        )
        return resultado