from modelos.enums import EstadoEntrada
from modelos.sala import Asiento
from modelos.venta import Entrada
from repositorios.entrada_repositorio import EntradaRepositorio
from servicios.auditoria_servicio import AuditoriaServicio

class EntradaServicio:
    def __init__(self):
        self.__repo = EntradaRepositorio()
        self.__auditoria= AuditoriaServicio()

    def validar(self, codigo, id_usuario=None):
        fila = self.__repo.buscar_por_codigo(codigo.strip())
        if fila is None:
            raise ValueError("Entrada inexistente")

        # Convertimos la fila de la BD en un objeto Entrada del modelo
        entrada = Entrada(
            fila["id"],
            fila["codigo"],
            Asiento(fila["id_asiento"], "", 0),
            float(fila["precio"]),
            EstadoEntrada(fila["estado"]),
        )

        # La regla vive en el modelo: lanza ValueError si no está vendida
        entrada.marcar_usada()

        self.__repo.actualizar_estado(entrada.id, entrada.estado.value)
        self.__auditoria.registrar("VALIDAR_ENTRADA", f"Ingreso permitido {entrada.codigo}", id_usuario)
        return {"codigo": entrada.codigo, "estado": entrada.estado.value}