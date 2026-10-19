from flask import Blueprint, jsonify
from repositorios.obra_repositorio import ObraRepositorio

obras_bp = Blueprint("obras", __name__)
repositorio = ObraRepositorio()


@obras_bp.route("/api/obras")
def listar_obras():
    obras = repositorio.listar_activas()
    return jsonify([obra.to_dict() for obra in obras])