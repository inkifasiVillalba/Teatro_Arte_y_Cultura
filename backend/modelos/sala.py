class Asiento:
    def __init__(self, id, fila, numero, ubicacion="Platea General"):
        self.__id = id
        self.__fila = fila
        self.__numero = numero
        self.__ubicacion = ubicacion

    @property
    def id(self):
        return self.__id

    def obtener_codigo(self):
        return f"{self.__fila}-{self.__numero}"

    def to_dict(self):
        return {
            "id": self.__id,
            "fila": self.__fila,
            "numero": self.__numero,
            "ubicacion": self.__ubicacion,
            "codigo": self.obtener_codigo(),
        }


class Sala:
    def __init__(self, id, nombre, capacidad):
        self.__id = id
        self.__nombre = nombre
        self.__capacidad = capacidad
        self.__asientos = []

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def asientos(self):
        return self.__asientos

    def agregar_asiento(self, asiento):
        self.__asientos.append(asiento)

    def consultar_capacidad(self):
        return self.__capacidad

    def to_dict(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "capacidad": self.__capacidad,
        }