import hashlib
from modelos.usuario import Empleado, Administrador
from repositorios.usuario_repositorio import UsuarioRepositorio


class UsuarioServicio:
    """Gestión de usuarios: solo un administrador activo puede ver y crear personal."""

    ROLES_PERSONAL = ("EMPLEADO", "ADMINISTRADOR")

    def __init__(self):
        self.__repo = UsuarioRepositorio()

    def __exigir_administrador(self, id_admin):
        fila = self.__repo.buscar_por_id(id_admin) if id_admin else None
        if fila is None or fila["rol"] != "ADMINISTRADOR" or not fila["activo"]:
            raise PermissionError("Solo un administrador puede gestionar usuarios")

    def listar(self, id_admin):
        self.__exigir_administrador(id_admin)
        usuarios = []
        for f in self.__repo.listar():
            if f["cargo"]:
                detalle = f["cargo"]
            elif f["telefono"]:
                detalle = f["telefono"]
            elif f["nivel_acceso"]:
                detalle = f"Nivel {f['nivel_acceso']}"
            else:
                detalle = "—"
            ultimo = f["ultimo_acceso"]
            usuarios.append({
                "id": f["id"],
                "nombre": f["nombre"],
                "correo": f["correo"],
                "rol": f["rol"],
                "detalle": detalle,
                "activo": bool(f["activo"]),
                "ultimo_acceso": ultimo.strftime("%Y-%m-%d %H:%M") if ultimo else "—",
            })
        return usuarios

    def registrar_personal(self, id_admin, nombre, correo, clave, confirmar, rol, cargo):
        self.__exigir_administrador(id_admin)

        nombre = nombre.strip()
        correo = correo.strip().lower()
        rol = rol.strip().upper()
        cargo = cargo.strip()

        if rol not in self.ROLES_PERSONAL:
            raise ValueError("El rol debe ser EMPLEADO o ADMINISTRADOR")
        if not nombre or not correo or not clave:
            raise ValueError("Nombre, correo y clave son obligatorios")
        if "@" not in correo or "." not in correo:
            raise ValueError("El correo no es válido")
        if len(clave) < 4:
            raise ValueError("La clave debe tener mínimo 4 caracteres")
        if clave != confirmar:
            raise ValueError("Las claves no coinciden")
        if rol == "EMPLEADO" and not cargo:
            raise ValueError("El cargo del empleado es obligatorio")
        if self.__repo.buscar_por_correo(correo) is not None:
            raise ValueError("Ya existe un usuario con ese correo")

        clave_hash = hashlib.sha256(clave.encode()).hexdigest()
        if rol == "EMPLEADO":
            nuevo_id = self.__repo.crear_personal(nombre, correo, clave_hash, rol, cargo, None)
            return Empleado(nuevo_id, nombre, correo, "", cargo).to_dict()
        nuevo_id = self.__repo.crear_personal(nombre, correo, clave_hash, rol, None, 1)
        return Administrador(nuevo_id, nombre, correo, "", 1).to_dict()