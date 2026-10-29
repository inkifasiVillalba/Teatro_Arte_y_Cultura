from modelos.producto import Producto
from repositorios.dashboard_repositorio import DashboardRepositorio
from repositorios.producto_repositorio import ProductoRepositorio


class DashboardServicio:
    def __init__(self):
        self.__repo = DashboardRepositorio()
        self.__productos = ProductoRepositorio()

    def resumen(self):
        datos = self.__repo.indicadores()

        salas = []
        for fila in self.__repo.ocupacion_por_sala():
            cupos = fila["capacidad"] * fila["funciones"]
            vendidos = int(fila["vendidos"])
            salas.append({
                "nombre": fila["nombre"],
                "capacidad": fila["capacidad"],
                "funciones": fila["funciones"],
                "cupos": cupos,
                "vendidos": vendidos,
                "porcentaje": round(vendidos / cupos * 100) if cupos else 0,
            })
        datos["salas"] = salas

        # Regla R7: alertas de reabastecimiento según la cantidad mínima de cada producto
        inventario = []
        for f in self.__productos.listar_activos():
            producto = Producto(f["id"], f["nombre"], f["categoria"], float(f["precio"]),
                                f["existencias"], f["activo"], f["stock_minimo"])
            inventario.append(producto.to_dict())
        datos["inventario"] = inventario
        return datos
