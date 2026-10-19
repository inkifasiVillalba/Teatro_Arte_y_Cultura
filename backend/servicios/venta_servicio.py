from repositorios.venta_repositorio import VentaRepositorio


class VentaServicio:
    def __init__(self):
        self.__repo = VentaRepositorio()

    def comprar(self, id_cliente, id_funcion, asientos, precio, metodo):
        if not asientos:
            raise ValueError("Debes elegir al menos un asiento")
        if metodo not in ("EFECTIVO", "TARJETA", "TRANSFERENCIA"):
            raise ValueError("Método de pago no válido")
        return self.__repo.guardar_compra(
            id_cliente, id_funcion, asientos, precio, metodo
        )