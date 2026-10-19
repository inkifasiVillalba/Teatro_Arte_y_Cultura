from modelos.obra import Obra
from repositorios.obra_repositorio import ObraRepositorio


class ObraServicio:
    def __init__(self):
        self.__repo = ObraRepositorio()

    def crear_obra(self, titulo, genero, clasificacion, director, descripcion, duracion):
        titulo = titulo.strip()
        if not titulo or not director.strip():
            raise ValueError("Título y director son obligatorios")
        try:
            duracion = int(duracion)
        except (TypeError, ValueError):
            raise ValueError("La duración debe ser un número")
        if duracion <= 0:
            raise ValueError("La duración debe ser mayor a cero")

        # Regla R1: no se permiten títulos duplicados
        if self.__repo.existe_titulo(titulo):
            raise ValueError("Ya existe una obra con ese título")

        nuevo_id = self.__repo.crear(titulo, genero, clasificacion, director, descripcion, duracion)
        obra = Obra(nuevo_id, titulo, genero, clasificacion, director, descripcion, duracion)
        return obra.to_dict()