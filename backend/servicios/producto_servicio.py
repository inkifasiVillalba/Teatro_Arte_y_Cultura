from modelos.producto import Producto
from repositorios.producto_repositorio import ProductoRepositorio


class ProductoServicio:
    def __init__(self):
        self.__repo = ProductoRepositorio()

    def listar(self):
        filas = self.__repo.listar_activos()
        productos = [
            Producto(f["id"], f["nombre"], f["categoria"],
                     float(f["precio"]), f["existencias"], f["activo"])
            for f in filas
        ]
        return [p.to_dict() for p in productos]

    def vender(self, id_producto, cantidad):
        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            raise ValueError("La cantidad debe ser un número")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")

        fila = self.__repo.buscar_por_id(id_producto)
        if fila is None:
            raise ValueError("Producto inexistente")

        # Convertimos la fila en un objeto Producto del modelo
        producto = Producto(fila["id"], fila["nombre"], fila["categoria"],
                            float(fila["precio"]), fila["existencias"], fila["activo"])

        # La regla R7 vive en el modelo: lanza ValueError si no hay stock
        producto.descontar_stock(cantidad)

        self.__repo.actualizar_existencias(producto.id, producto.existencias)
        return {
            "producto": producto.nombre,
            "cantidad": cantidad,
            "total": producto.precio * cantidad,
            "existencias": producto.existencias,
        }