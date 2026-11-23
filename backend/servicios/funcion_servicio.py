from datetime import datetime, timedelta
from modelos.funcion import Funcion
from modelos.obra import Obra
from repositorios.funcion_repositorio import FuncionRepositorio
from repositorios.obra_repositorio import ObraRepositorio
from repositorios.sala_repositorio import SalaRepositorio
from servicios.auditoria_servicio import AuditoriaServicio

class FuncionServicio:
    def __init__(self):
        self.__repo = FuncionRepositorio()
        self.__obras = ObraRepositorio()
        self.__salas = SalaRepositorio()
        self.__auditoria = AuditoriaServicio()

    def listar(self):
        filas = self.__repo.listar_todas()
        ahora = datetime.now()
        resultado = []
        for f in filas:
            inicio = f["fecha_hora"]
            fin = inicio + timedelta(minutes=f["duracion_min"])
            ocupacion = round(f["vendidas"] / f["capacidad"] * 100) if f["capacidad"] else 0

            # Estado real según la hora actual (las canceladas se respetan)
            estado = f["estado"]
            if estado != "CANCELADA":
                if ahora >= fin:
                    estado = "FINALIZADA"
                elif ahora >= inicio:
                    estado = "EN_CURSO"

            resultado.append({
                "id": f["id"],
                "obra": f["titulo"],
                "sala": f["sala"],
                "fecha": inicio.strftime("%Y-%m-%d"),
                "horario": f"{inicio.strftime('%H:%M')} - {fin.strftime('%H:%M')}",
                "precio": float(f["precio"]),
                "ocupacion": f"{f['vendidas']} / {f['capacidad']} ({ocupacion}%)",
                "estado": estado,
            })

        # Las finalizadas van al final de la lista (el orden por fecha se mantiene)
        resultado.sort(key=lambda r: r["estado"] == "FINALIZADA")
        return resultado

    
    def programar(self, id_obra, id_sala, fecha_hora, precio, id_usuario=None):
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
        if fecha < datetime.now():
            raise ValueError("No puedes programar una función en una fecha pasada")

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
        self.__auditoria.registrar(
            "PROGRAMAR_FUNCION",
            f'"{obra.titulo}" programada en {sala.nombre} sin cruces ({fecha_hora})',
            id_usuario,
        )
        return {"id": nuevo_id, "obra": obra.titulo, "sala": sala.nombre}

    def cancelar(self, id_funcion, id_usuario=None):
        fila = self.__repo.buscar_por_id(id_funcion)
        if fila is None:
            raise ValueError("Función inexistente")
        if fila["estado"] == "CANCELADA":
            raise ValueError("La función ya está cancelada")
        if datetime.now() >= fila["fecha_hora"]:
            raise ValueError("No se puede cancelar una función que ya empezó o finalizó")
        if fila["vendidas"] > 0:
            raise ValueError("No se puede cancelar: ya tiene entradas vendidas")
        if fila["reservas"] > 0:
            raise ValueError("No se puede cancelar: tiene reservas pendientes")

        self.__repo.actualizar_estado(id_funcion, "CANCELADA")
        fecha = fila["fecha_hora"].strftime("%Y-%m-%d %H:%M")
        self.__auditoria.registrar(
            "CANCELAR_FUNCION",
            f'"{fila["titulo"]}" del {fecha} cancelada',
            id_usuario,
        )