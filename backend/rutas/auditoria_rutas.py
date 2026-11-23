from flask import Blueprint, request, jsonify
from servicios.auditoria_servicio import AuditoriaServicio

auditoria_bp = Blueprint("auditoria", __name__)
servicio = AuditoriaServicio()


@auditoria_bp.route("/api/auditoria")
def listar_auditoria():
    try:
        return jsonify(servicio.listar(request.args.get("id_admin", type=int)))
    except PermissionError as error:
        return jsonify({"error": str(error)}), 403