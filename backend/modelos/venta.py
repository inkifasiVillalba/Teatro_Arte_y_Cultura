from datetime import datetime
from modelos.enums import EstadoEntrada, EstadoPago, MetodoPago


class Entrada:
    def __init__(self, id, codigo, asiento, precio,
                 estado=EstadoEntrada.VENDIDA):
        self.__id = id
        self.__codigo = codigo          # ej: TAC-2026-F1-C4
        self.__asiento = asiento        # objeto Asiento
        self.__precio = precio
        self.__estado = estado

    @property
    def id(self):
        return self.__id

    @property
    def codigo(self):
        return self.__codigo

    @property
    def asiento(self):
        return self.__asiento

    @property
    def precio(self):
        return self.__precio

    @property
    def estado(self):
        return self.__estado

    def marcar_usada(self):
        if self.__estado != EstadoEntrada.VENDIDA:
            raise ValueError("Solo una entrada vendida puede usarse")
        self.__estado = EstadoEntrada.USADA

    def anular(self):
        if self.__estado == EstadoEntrada.USADA:
            raise ValueError("No se puede anular una entrada ya usada")
        self.__estado = EstadoEntrada.ANULADA

    def to_dict(self):
        return {
            "id": self.__id,
            "codigo": self.__codigo,
            "asiento": self.__asiento.obtener_codigo(),
            "precio": self.__precio,
            "estado": self.__estado.value,
        }


class DetalleVentaProducto:
    def __init__(self, producto, cantidad):
        self.__producto = producto      # objeto Producto
        self.__cantidad = cantidad
        self.__precio_unitario = producto.precio

    @property
    def producto(self):
        return self.__producto

    @property
    def cantidad(self):
        return self.__cantidad

    def subtotal(self):
        return self.__precio_unitario * self.__cantidad

    def to_dict(self):
        return {
            "producto": self.__producto.nombre,
            "cantidad": self.__cantidad,
            "precio_unitario": self.__precio_unitario,
            "subtotal": self.subtotal(),
        }


class Pago:
    def __init__(self, id, monto, metodo, estado=EstadoPago.PENDIENTE):
        self.__id = id
        self.__monto = monto
        self.__metodo = metodo          # MetodoPago
        self.__fecha = datetime.now()
        self.__estado = estado

    @property
    def monto(self):
        return self.__monto

    @property
    def metodo(self):
        return self.__metodo

    @property
    def estado(self):
        return self.__estado

    def registrar(self):
        """Aprueba el pago (aquí iría la validación real con el banco)."""
        if self.__monto <= 0:
            self.__estado = EstadoPago.RECHAZADO
            return False
        self.__estado = EstadoPago.APROBADO
        return True

    def anular(self):
        if self.__estado != EstadoPago.APROBADO:
            raise ValueError("Solo se puede anular un pago aprobado")
        self.__estado = EstadoPago.ANULADO

    def to_dict(self):
        return {
            "id": self.__id,
            "monto": self.__monto,
            "metodo": self.__metodo.value,
            "fecha": self.__fecha.isoformat(),
            "estado": self.__estado.value,
        }


class Venta:
    def __init__(self, id, cliente=None):
        self.__id = id
        self.__cliente = cliente
        self.__fecha = datetime.now()
        self.__entradas = []            # lista de Entrada
        self.__productos = []           # lista de DetalleVentaProducto
        self.__pago = None

    @property
    def id(self):
        return self.__id

    @property
    def entradas(self):
        return self.__entradas

    @property
    def productos(self):
        return self.__productos

    @property
    def pago(self):
        return self.__pago

    def agregar_entrada(self, entrada):
        self.__entradas.append(entrada)

    def agregar_producto(self, producto, cant):
        # Regla R7: descuenta stock y prohíbe la sobreventa
        producto.descontar_stock(cant)
        self.__productos.append(DetalleVentaProducto(producto, cant))

    def calcular_total(self):
        total_entradas = sum(e.precio for e in self.__entradas)
        total_productos = sum(p.subtotal() for p in self.__productos)
        return total_entradas + total_productos

    def pagar(self, metodo):
        if self.__pago is not None:
            raise ValueError("Esta venta ya tiene un pago registrado")
        if self.calcular_total() <= 0:
            raise ValueError("No hay nada que cobrar en esta venta")
        pago = Pago(self.__id, self.calcular_total(), metodo)
        pago.registrar()
        self.__pago = pago
        return pago

    def to_dict(self):
        return {
            "id": self.__id,
            "cliente": self.__cliente.nombre if self.__cliente else None,
            "fecha": self.__fecha.isoformat(),
            "entradas": [e.to_dict() for e in self.__entradas],
            "productos": [p.to_dict() for p in self.__productos],
            "total": self.calcular_total(),
            "pago": self.__pago.to_dict() if self.__pago else None,
        }