from enum import Enum


class EstadoFuncion(Enum):
    PROGRAMADA = "PROGRAMADA"
    EN_CURSO = "EN_CURSO"
    FINALIZADA = "FINALIZADA"
    CANCELADA = "CANCELADA"


class EstadoReserva(Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    EXPIRADA = "EXPIRADA"


class EstadoEntrada(Enum):
    VENDIDA = "VENDIDA"
    USADA = "USADA"
    ANULADA = "ANULADA"


class EstadoPago(Enum):
    PENDIENTE = "PENDIENTE"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"
    ANULADO = "ANULADO"


class MetodoPago(Enum):
    EFECTIVO = "EFECTIVO"
    TARJETA = "TARJETA"
    TRANSFERENCIA = "TRANSFERENCIA"