import hashlib
from modelos.usuario import Cliente, Empleado, Administrador
from repositorios.usuario_repositorio import UsuarioRepositorio


class AutenticacionServicio:
    def __init__(self):
        self.__repo = UsuarioRepositorio()

    def __fila_a_objeto(self, fila):
        """Convierte una fila de la BD en Cliente, Empleado o Administrador."""
        rol = fila["rol"]
        base = (fila["id"], fila["nombre"], fila["correo"], "")
        if rol == "CLIENTE":
            return Cliente(*base, fila["telefono"])
        if rol == "EMPLEADO":
            return Empleado(*base, fila["cargo"])
        return Administrador(*base, fila["nivel_acceso"])

    def iniciar_sesion(self, correo, clave, rol):
        fila = self.__repo.buscar_por_correo(correo)
        if fila is None or not fila["activo"] or fila["rol"] != rol:
            return None

        hash_recibido = hashlib.sha256(clave.encode()).hexdigest()
        if hash_recibido != fila["clave_hash"]:
            return None

        self.__repo.actualizar_ultimo_acceso(fila["id"])
        return self.__fila_a_objeto(fila).to_dict()


    def registrar_cliente(self, nombre, correo, telefono, clave, confirmar):
        nombre = nombre.strip()
        correo = correo.strip().lower()

        if not nombre or not correo or not clave:
            raise ValueError("Nombre, correo y clave son obligatorios")
        if "@" not in correo or "." not in correo:
            raise ValueError("El correo no es válido")
        if len(clave) < 4:
            raise ValueError("La clave debe tener mínimo 4 caracteres")
        if clave != confirmar:
            raise ValueError("Las claves no coinciden")
        if self.__repo.buscar_por_correo(correo) is not None:
            raise ValueError("Ya existe un usuario con ese correo")

        clave_hash = hashlib.sha256(clave.encode()).hexdigest()
        nuevo_id = self.__repo.crear_cliente(nombre, correo, clave_hash, telefono)
        return Cliente(nuevo_id, nombre, correo, "", telefono).to_dict() 