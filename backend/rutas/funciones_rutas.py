from flask import Blueprint, jsonify
from repositorios.funcion_repositorio import FuncionRepositorio

funciones_bp = Blueprint("funciones", __name__)
repositorio = FuncionRepositorio()


@funciones_bp.route("/api/obras/<int:id_obra>/funciones")
def funciones_de_obra(id_obra):
    filas = repositorio.listar_por_obra(id_obra)
    for f in filas:
        f["fecha_hora"] = f["fecha_hora"].strftime("%Y-%m-%d %H:%M")
        f["precio"] = float(f["precio"])
    return jsonify(filas)


@funciones_bp.route("/api/funciones/<int:id_funcion>/asientos")
def asientos_de_funcion(id_funcion):
    return jsonify(repositorio.listar_asientos(id_funcion))