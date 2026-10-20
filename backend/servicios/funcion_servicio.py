from datetime import datetime, timedelta
from modelos.funcion import Funcion
from modelos.obra import Obra
from repositorios.funcion_repositorio import FuncionRepositorio
from repositorios.obra_repositorio import ObraRepositorio
from repositorios.sala_repositorio import SalaRepositorio


class FuncionServicio:
    def __init__(self):
        self.__repo = FuncionRepositorio()
        self.__obras = ObraRepositorio()
        self.__salas = SalaRepositorio()

    def listar(self):
        filas = self.__repo.listar_todas()
        resultado = []
        for f in filas:
            fin = f["fecha_hora"] + timedelta(minutes=f["duracion_min"])
            ocupacion = round(f["vendidas"] / f["capacidad"] * 100) if f["capacidad"] else 0
            resultado.append({
                "id": f["id"],
                "obra": f["titulo"],
                "sala": f["sala"],
                "fecha": f["fecha_hora"].strftime("%Y-%m-%d"),
                "horario": f"{f['fecha_hora'].strftime('%H:%M')} - {fin.strftime('%H:%M')}",
                "precio": float(f["precio"]),
                "ocupacion": f"{f['vendidas']} / {f['capacidad']} ({ocupacion}%)",
                "estado": f["estado"],
            })
        return resultado

    def programar(self, id_obra, id_sala, fecha_hora, precio):
        # Validaciones básicas
        try:
            fecha = datetime.strptime(fecha_hora, "%Y-%m-%dT%H:%M")
            precio = float(precio)
            id_obra = int(id_obra)
            id_sala = int(id_sala)
        except (TypeError, ValueError):
            raise ValueError("Revisa obra, sala, fecha, hora y precio")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a cero")

        obra = self.__obras.buscar_por_id(id_obra)
        sala = self.__salas.buscar_por_id(id_sala)
        if obra is None or sala is None:
            raise ValueError("Obra o sala inexistente")

        # Objeto Funcion nuevo (aún sin guardar)
        nueva = Funcion(0, obra, sala, fecha, precio)

        # Regla R3: no puede cruzarse con otra función de la misma sala
        for fila in self.__repo.listar_de_sala(id_sala):
            obra_existente = Obra(0, fila["titulo"], "", "", "", "", fila["duracion_min"])
            existente = Funcion(fila["id"], obra_existente, sala,
                                fila["fecha_hora"], float(fila["precio"]))
            if nueva.se_cruza_con(existente):
                raise ValueError(
                    f"Cruce de horario con \"{fila['titulo']}\" "
                    f"({fila['fecha_hora'].strftime('%Y-%m-%d %H:%M')}). "
                    f"Recuerda el intervalo de {Funcion.INTERVALO_MIN} minutos."
                )

        nuevo_id = self.__repo.crear(id_obra, id_sala, fecha, precio)
        return {"id": nuevo_id, "obra": obra.titulo, "sala": sala.nombre}