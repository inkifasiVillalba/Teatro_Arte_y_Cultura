from datetime import datetime
import hashlib


class Usuario:
    def __init__(self, id, nombre, correo, clave, activo=True):
        self.__id = id
        self.__nombre = nombre
        self.__correo = correo
        self.__clave_hash = self.__encriptar(clave)
        self.__activo = activo
        self.__ultimo_acceso = None

    # Método privado: convierte la clave en un código irreconocible
    def __encriptar(self, clave):
        return hashlib.sha256(clave.encode()).hexdigest()

    # Getters (para leer los atributos privados desde fuera)
    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def activo(self):
        return self.__activo

    def iniciar_sesion(self, clave):
        if self.__activo and self.__encriptar(clave) == self.__clave_hash:
            self.__ultimo_acceso = datetime.now()
            return True
        return False

    def cerrar_sesion(self):
        pass

    def cambiar_clave(self, nueva):
        self.__clave_hash = self.__encriptar(nueva)

    def to_dict(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "correo": self.__correo,
            "activo": self.__activo,
        }


class Cliente(Usuario):
    def __init__(self, id, nombre, correo, clave, telefono):
        super().__init__(id, nombre, correo, clave)
        self.__telefono = telefono

    def to_dict(self):
        datos = super().to_dict()
        datos["rol"] = "CLIENTE"
        datos["telefono"] = self.__telefono
        return datos


class Empleado(Usuario):
    def __init__(self, id, nombre, correo, clave, cargo):
        super().__init__(id, nombre, correo, clave)
        self.__cargo = cargo

    def to_dict(self):
        datos = super().to_dict()
        datos["rol"] = "EMPLEADO"
        datos["cargo"] = self.__cargo
        return datos


class Administrador(Usuario):
    def __init__(self, id, nombre, correo, clave, nivel_acceso):
        super().__init__(id, nombre, correo, clave)
        self.__nivel_acceso = nivel_acceso

    def to_dict(self):
        datos = super().to_dict()
        datos["rol"] = "ADMINISTRADOR"
        datos["nivel_acceso"] = self.__nivel_acceso
        return datos