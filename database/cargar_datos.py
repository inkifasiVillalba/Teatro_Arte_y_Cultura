import hashlib
import sys
import os

import mysql.connector

# Permite importar config desde la carpeta backend
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))
from config import DB_CONFIG


def encriptar(clave):
    # Mismo método que usa la clase Usuario
    return hashlib.sha256(clave.encode()).hexdigest()


# (id_sala, filas, columnas)
SALAS = [
    (1, "ABCDEF", 8),   # Principal: 6 filas x 8 = 48
    (2, "ABCD", 8),     # Experimental: 4 filas x 8 = 32
    (3, "ABC", 8),      # Palco VIP: 3 filas x 8 = 24
]

USUARIOS = [
    ("Dra. Beatriz Helena Morales", "admin@teatroarteycultura.com",
     "admin123", "ADMINISTRADOR", None, None, 3),
    ("Juan Camilo Quintero", "taquilla@teatroarteycultura.com",
     "emp123", "EMPLEADO", None, "Taquillero Principal", None),
    ("Mariana Restrepo Gómez", "cliente@gmail.com",
     "cli123", "CLIENTE", "+573148924511", None, None),
]


def main():
    conexion = mysql.connector.connect(**DB_CONFIG)
    cursor = conexion.cursor()

    # Asientos
    for id_sala, filas, columnas in SALAS:
        for fila in filas:
            for numero in range(1, columnas + 1):
                cursor.execute(
                    "INSERT IGNORE INTO asientos (id_sala, fila, numero) "
                    "VALUES (%s, %s, %s)",
                    (id_sala, fila, numero),
                )

    # Usuarios demo
    for nombre, correo, clave, rol, tel, cargo, nivel in USUARIOS:
        cursor.execute(
            "INSERT IGNORE INTO usuarios "
            "(nombre, correo, clave_hash, rol, telefono, cargo, nivel_acceso) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (nombre, correo, encriptar(clave), rol, tel, cargo, nivel),
        )

    conexion.commit()

    cursor.execute("SELECT COUNT(*) FROM asientos")
    print("Asientos:", cursor.fetchone()[0])
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    print("Usuarios:", cursor.fetchone()[0])

    cursor.close()
    conexion.close()


if __name__ == "__main__":
    main()