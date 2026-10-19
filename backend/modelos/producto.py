class Producto:
    def __init__(self, id, nombre, categoria, precio, existencias, activo=True):
        self.__id = id
        self.__nombre = nombre
        self.__categoria = categoria
        self.__precio = precio
        self.__existencias = existencias
        self.__activo = activo

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def precio(self):
        return self.__precio

    @property
    def existencias(self):
        return self.__existencias

    def hay_stock(self, cant):
        return self.__activo and self.__existencias >= cant

    def descontar_stock(self, cant):
        if not self.hay_stock(cant):
            raise ValueError(f"No hay suficiente stock de {self.__nombre}")
        self.__existencias -= cant

    def to_dict(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "categoria": self.__categoria,
            "precio": self.__precio,
            "existencias": self.__existencias,
            "activo": self.__activo,
        }