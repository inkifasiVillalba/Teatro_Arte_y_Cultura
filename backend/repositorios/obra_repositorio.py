import mysql.connector
from config import DB_CONFIG
from modelos.obra import Obra


class ObraRepositorio:
    def listar_activas(self):
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM obras WHERE activa = TRUE")
        filas = cursor.fetchall()
        cursor.close()
        conexion.close()
        # Cada fila de la tabla se convierte en un objeto Obra
        return [Obra(**fila) for fila in filas]

    def existe_titulo(self, titulo):
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM obras WHERE LOWER(titulo) = LOWER(%s)", (titulo,))
        cantidad = cursor.fetchone()[0]
        cursor.close()
        conexion.close()
        return cantidad > 0

    def crear(self, titulo, genero, clasificacion, director, descripcion, duracion_min):
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO obras (titulo, genero, clasificacion, director, descripcion, duracion_min) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (titulo, genero, clasificacion, director, descripcion, duracion_min),
        )
        conexion.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        conexion.close()
        return nuevo_id



    def buscar_por_id(self, id_obra):
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM obras WHERE id = %s", (id_obra,))
        fila = cursor.fetchone()
        cursor.close()
        conexion.close()
        return Obra(**fila) if fila else None
    
    def actualizar_activa(self, id_obra, activa):
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        cursor.execute("UPDATE obras SET activa = %s WHERE id = %s", (activa, id_obra))
        conexion.commit()
        cursor.close()
        conexion.close()


    