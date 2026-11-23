from modelos.auditoria import RegistroOperacion
from repositorios.auditoria_repositorio import AuditoriaRepositorio
from repositorios.usuario_repositorio import UsuarioRepositorio


class AuditoriaServicio:
    def __init__(self):
        self.__repo = AuditoriaRepositorio()
        self.__usuarios = UsuarioRepositorio()

    def registrar(self, accion, detalle, id_usuario=None):
        """Guarda la operación. Si falla, NO debe afectar la operación principal."""
        try:
            registro = RegistroOperacion(accion, detalle).to_dict()
            self.__repo.registrar(registro["accion"], registro["detalle"], id_usuario)
        except Exception as error:
            print(f"[AUDITORIA] No se pudo registrar: {error}")

    def listar(self, id_admin, limite=100):
        fila = self.__usuarios.buscar_por_id(id_admin) if id_admin else None
        if fila is None or fila["rol"] != "ADMINISTRADOR" or not fila["activo"]:
            raise PermissionError("Solo un administrador puede ver la auditoría")
        return [
            {
                "id": f["id"],
                "fecha": f["fecha"].strftime("%Y-%m-%d %H:%M:%S"),
                "usuario": f["usuario"] or "Sistema",
                "accion": f["accion"],
                "detalle": f["detalle"],
            }
            for f in self.__repo.listar(limite)
        ]