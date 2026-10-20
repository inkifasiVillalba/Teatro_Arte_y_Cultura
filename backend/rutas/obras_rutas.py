from flask import Blueprint, jsonify, request
from repositorios.obra_repositorio import ObraRepositorio
from servicios.obra_servicio import ObraServicio

obras_bp = Blueprint("obras", __name__)
repositorio = ObraRepositorio()


@obras_bp.route("/api/obras")
def listar_obras():
    obras = repositorio.listar_activas()
    return jsonify([obra.to_dict() for obra in obras])



servicio = ObraServicio()


@obras_bp.route("/api/obras", methods=["POST"])
def crear_obra():
    datos = request.get_json() or {}
    try:
        obra = servicio.crear_obra(
            datos.get("titulo", ""),
            datos.get("genero", ""),
            datos.get("clasificacion", ""),
            datos.get("director", ""),
            datos.get("descripcion", ""),
            datos.get("duracion_min", 0),
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(obra), 201


@obras_bp.route("/api/obras/<int:id_obra>/desactivar", methods=["POST"])
def desactivar_obra(id_obra):
    try:
        servicio.desactivar(id_obra)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"mensaje": "Obra desactivada"})