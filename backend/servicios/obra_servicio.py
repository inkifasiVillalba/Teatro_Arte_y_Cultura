from modelos.obra import Obra
from repositorios.obra_repositorio import ObraRepositorio
from servicios.auditoria_servicio import AuditoriaServicio

class ObraServicio:
    def __init__(self):
        self.__repo = ObraRepositorio()
        self.__auditoria = AuditoriaServicio()

    def crear_obra(self, titulo, genero, clasificacion, director, descripcion, duracion, id_usuario=None):
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
        self.__auditoria.registrar("CREAR_OBRA", f'Obra "{titulo}" ({genero})', id_usuario)
        return obra.to_dict()
       
    


    def desactivar(self, id_obra, id_usuario= None):
        obra = self.__repo.buscar_por_id(id_obra)
        if obra is None:
            raise ValueError("Obra inexistente")
        obra.desactivar()   # la regla vive en el modelo
        self.__repo.actualizar_activa(obra.id, obra.activa)
        self.__auditoria.registrar("DESACTIVAR_OBRA", f'Obra "{obra.titulo}" desactivada', id_usuario)