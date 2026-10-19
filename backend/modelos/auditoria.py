from datetime import datetime


class RegistroOperacion:
    __contador = 0  # atributo de clase: genera ids automáticos

    def __init__(self, accion, detalle, usuario=None):
        RegistroOperacion.__contador += 1
        self.__id = RegistroOperacion.__contador
        self.__fecha = datetime.now()
        self.__accion = accion          # ej: CREAR_OBRA, VENTA_TAQUILLA
        self.__detalle = detalle
        self.__usuario = usuario        # objeto Usuario (opcional)

    @property
    def id(self):
        return self.__id

    @property
    def accion(self):
        return self.__accion

    @staticmethod
    def registrar(lista, accion, detalle, usuario=None):
        """Crea un registro y lo agrega a una lista (el libro de auditoría)."""
        registro = RegistroOperacion(accion, detalle, usuario)
        lista.append(registro)
        return registro

    def to_dict(self):
        return {
            "id": self.__id,
            "fecha": self.__fecha.isoformat(),
            "accion": self.__accion,
            "detalle": self.__detalle,
            "usuario": self.__usuario.nombre if self.__usuario else None,
        }


class Reporte:
    def __init__(self, tipo, ventas, funciones, productos):
        self.__tipo = tipo
        self.__fecha_generacion = datetime.now()
        self.__ventas = ventas          # lista de Venta
        self.__funciones = funciones    # lista de Funcion
        self.__productos = productos    # lista de Producto

    def ventas_por_periodo(self, desde=None, hasta=None):
        total = 0.0
        for v in self.__ventas:
            if v.pago is None:
                continue
            fecha = datetime.fromisoformat(v.to_dict()["fecha"])
            if desde and fecha < desde:
                continue
            if hasta and fecha > hasta:
                continue
            total += v.calcular_total()
        return total

    def ocupacion_salas(self):
        if not self.__funciones:
            return 0.0
        promedio = sum(f.ocupacion() for f in self.__funciones) / len(self.__funciones)
        return round(promedio, 1)

    def productos_mas_vendidos(self):
        conteo = {}
        for v in self.__ventas:
            for d in v.productos:
                nombre = d.producto.nombre
                conteo[nombre] = conteo.get(nombre, 0) + d.cantidad
        return sorted(conteo.items(), key=lambda x: x[1], reverse=True)

    def generar(self):
        return {
            "tipo": self.__tipo,
            "fecha_generacion": self.__fecha_generacion.isoformat(),
            "ventas_total": self.ventas_por_periodo(),
            "ocupacion_promedio": self.ocupacion_salas(),
            "productos_mas_vendidos": self.productos_mas_vendidos(),
        }