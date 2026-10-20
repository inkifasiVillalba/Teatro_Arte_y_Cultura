from flask import Blueprint, jsonify, request
from repositorios.funcion_repositorio import FuncionRepositorio
from servicios.funcion_servicio import FuncionServicio
from repositorios.obra_repositorio import ObraRepositorio
from repositorios.sala_repositorio import SalaRepositorio

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


servicio = FuncionServicio()


@funciones_bp.route("/api/funciones")
def listar_funciones():
    return jsonify(servicio.listar())


@funciones_bp.route("/api/funciones", methods=["POST"])
def programar_funcion():
    d = request.get_json() or {}
    try:
        resultado = servicio.programar(
            d.get("id_obra"), d.get("id_sala"), d.get("fecha_hora"), d.get("precio")
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(resultado), 201


@funciones_bp.route("/api/salas")
def listar_salas():
    return jsonify([s.to_dict() for s in SalaRepositorio().listar()])