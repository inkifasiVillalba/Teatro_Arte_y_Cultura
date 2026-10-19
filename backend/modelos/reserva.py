from datetime import datetime
from modelos.enums import EstadoReserva


class DetalleReserva:
    def __init__(self, id, asiento, precio):
        self.__id = id
        self.__asiento = asiento    # objeto Asiento
        self.__precio = precio

    @property
    def id(self):
        return self.__id

    @property
    def asiento(self):
        return self.__asiento

    def obtener_subtotal(self):
        return self.__precio

    def to_dict(self):
        return {
            "id": self.__id,
            "asiento": self.__asiento.obtener_codigo(),
            "precio": self.__precio,
        }


class Reserva:
    def __init__(self, id, cliente, funcion, estado=EstadoReserva.PENDIENTE):
        self.__id = id
        self.__cliente = cliente        # objeto Cliente
        self.__funcion = funcion        # objeto Funcion
        self.__fecha_reserva = datetime.now()
        self.__estado = estado
        self.__detalles = []            # lista de DetalleReserva

    @property
    def id(self):
        return self.__id

    @property
    def cliente(self):
        return self.__cliente

    @property
    def funcion(self):
        return self.__funcion

    @property
    def estado(self):
        return self.__estado

    @property
    def detalles(self):
        return self.__detalles

    def agregar_asiento(self, asiento):
        if self.__estado != EstadoReserva.PENDIENTE:
            raise ValueError("Solo se pueden agregar asientos a una reserva pendiente")
        if not self.__funcion.asiento_disponible(asiento):
            raise ValueError(f"El asiento {asiento.obtener_codigo()} no está disponible")
        if asiento.id in [d.asiento.id for d in self.__detalles]:
            raise ValueError("Ese asiento ya está en la reserva")
        detalle = DetalleReserva(len(self.__detalles) + 1, asiento, self.__funcion.precio)
        self.__detalles.append(detalle)

    def calcular_total(self):
        return sum(d.obtener_subtotal() for d in self.__detalles)

    def cancelar(self):
        if self.__estado != EstadoReserva.PENDIENTE:
            raise ValueError("Solo se puede cancelar una reserva pendiente")
        self.__estado = EstadoReserva.CANCELADA

    def marcar_confirmada(self):
        if self.__estado != EstadoReserva.PENDIENTE:
            raise ValueError("Solo se puede confirmar una reserva pendiente")
        self.__estado = EstadoReserva.CONFIRMADA

    def to_dict(self):
        return {
            "id": self.__id,
            "cliente": self.__cliente.nombre,
            "funcion": self.__funcion.id,
            "fecha_reserva": self.__fecha_reserva.isoformat(),
            "estado": self.__estado.value,
            "asientos": [d.to_dict() for d in self.__detalles],
            "total": self.calcular_total(),
        }