import mysql.connector
from config import DB_CONFIG


class UsuarioRepositorio:
    def __conectar(self):
        return mysql.connector.connect(**DB_CONFIG)

    def buscar_por_correo(self, correo):
        """Devuelve la fila del usuario como diccionario, o None."""
        conexion = self.__conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        fila = cursor.fetchone()
        cursor.close()
        conexion.close()
        return fila

    def actualizar_ultimo_acceso(self, id_usuario):
        conexion = self.__conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE usuarios SET ultimo_acceso = NOW() WHERE id = %s",
            (id_usuario,),
        )
        conexion.commit()
        cursor.close()
        conexion.close()


    def crear_cliente(self, nombre, correo, clave_hash, telefono):
        conexion = self.__conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, clave_hash, rol, telefono) "
            "VALUES (%s, %s, %s, 'CLIENTE', %s)",
            (nombre, correo, clave_hash, telefono),
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        conexion.close()
        return nuevo_id


    def buscar_por_id(self, id_usuario):
        conexion = self.__conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id_usuario,))
        fila = cursor.fetchone()
        cursor.close()
        conexion.close()
        return fila

    def listar(self):
        """Todos los usuarios, sin la clave."""
        conexion = self.__conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, nombre, correo, rol, telefono, cargo, nivel_acceso, activo, ultimo_acceso "
            "FROM usuarios ORDER BY FIELD(rol, 'ADMINISTRADOR', 'EMPLEADO', 'CLIENTE'), nombre"
        )
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return filas

    def crear_personal(self, nombre, correo, clave_hash, rol, cargo, nivel_acceso):
        """Crea un empleado o un administrador."""
        conexion = self.__conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, clave_hash, rol, cargo, nivel_acceso) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (nombre, correo, clave_hash, rol, cargo, nivel_acceso),
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        conexion.close()
        return nuevo_id