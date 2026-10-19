class Obra:
    def __init__(self, id, titulo, genero, clasificacion, director,
                 descripcion, duracion_min, activa=True):
        self.__id = id
        self.__titulo = titulo
        self.__genero = genero
        self.__clasificacion = clasificacion
        self.__director = director
        self.__descripcion = descripcion
        self.__duracion_min = duracion_min
        self.__activa = activa

    @property
    def id(self):
        return self.__id

    @property
    def titulo(self):
        return self.__titulo

    @property
    def duracion_min(self):
        return self.__duracion_min

    @property
    def activa(self):
        return self.__activa

    def obtener_ficha(self):
        return (f"{self.__titulo} ({self.__genero}, {self.__clasificacion}) "
                f"- Dirección: {self.__director} - {self.__duracion_min} min")

    def desactivar(self):
        self.__activa = False

    def to_dict(self):
        return {
            "id": self.__id,
            "titulo": self.__titulo,
            "genero": self.__genero,
            "clasificacion": self.__clasificacion,
            "director": self.__director,
            "descripcion": self.__descripcion,
            "duracion_min": self.__duracion_min,
            "activa": self.__activa,
        }