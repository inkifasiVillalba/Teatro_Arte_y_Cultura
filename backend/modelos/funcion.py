from datetime import timedelta
from modelos.enums import EstadoFuncion


class Funcion:
    INTERVALO_MIN = 30  # descanso obligatorio entre funciones (regla R3)

    def __init__(self, id, obra, sala, fecha_hora, precio,
                 estado=EstadoFuncion.PROGRAMADA):
        self.__id = id
        self.__obra = obra          # objeto Obra
        self.__sala = sala          # objeto Sala
        self.__fecha_hora = fecha_hora
        self.__precio = precio
        self.__estado = estado
        self.__asientos_ocupados = []   # lista de objetos Asiento

    @property
    def id(self):
        return self.__id

    @property
    def obra(self):
        return self.__obra

    @property
    def sala(self):
        return self.__sala

    @property
    def fecha_hora(self):
        return self.__fecha_hora

    @property
    def precio(self):
        return self.__precio

    @property
    def estado(self):
        return self.__estado

    def hora_fin(self):
        duracion = timedelta(minutes=self.__obra.duracion_min)
        return self.__fecha_hora + duracion

    def ocupar_asiento(self, asiento):
        if not self.asiento_disponible(asiento):
            raise ValueError(f"El asiento {asiento.obtener_codigo()} ya está ocupado")
        self.__asientos_ocupados.append(asiento)

    def asiento_disponible(self, asiento):
        return asiento.id not in [a.id for a in self.__asientos_ocupados]

    def asientos_libres(self):
        ocupados = [a.id for a in self.__asientos_ocupados]
        return [a for a in self.__sala.asientos if a.id not in ocupados]

    def ocupacion(self):
        capacidad = self.__sala.consultar_capacidad()
        if capacidad == 0:
            return 0.0
        return round(len(self.__asientos_ocupados) / capacidad * 100, 1)

    def se_cruza_con(self, otra):
        """True si esta función choca con otra en la misma sala."""
        if self.__sala.id != otra.sala.id:
            return False
        margen = timedelta(minutes=self.INTERVALO_MIN)
        inicio_a, fin_a = self.__fecha_hora, self.hora_fin() + margen
        inicio_b, fin_b = otra.fecha_hora, otra.hora_fin() + margen
        return inicio_a < fin_b and inicio_b < fin_a

    def to_dict(self):
        return {
            "id": self.__id,
            "obra": self.__obra.titulo,
            "sala": self.__sala.nombre,
            "fecha_hora": self.__fecha_hora.isoformat(),
            "hora_fin": self.hora_fin().isoformat(),
            "precio": self.__precio,
            "estado": self.__estado.value,
            "ocupacion": self.ocupacion(),
        }