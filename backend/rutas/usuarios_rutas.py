from flask import Blueprint, request, jsonify
from servicios.usuario_servicio import UsuarioServicio

usuarios_bp = Blueprint("usuarios", __name__)
servicio = UsuarioServicio()


@usuarios_bp.route("/api/usuarios")
def listar_usuarios():
    try:
        return jsonify(servicio.listar(request.args.get("id_admin", type=int)))
    except PermissionError as error:
        return jsonify({"error": str(error)}), 403


@usuarios_bp.route("/api/usuarios", methods=["POST"])
def crear_usuario():
    datos = request.get_json() or {}
    try:
        usuario = servicio.registrar_personal(
            datos.get("id_admin"),
            datos.get("nombre", ""),
            datos.get("correo", ""),
            datos.get("clave", ""),
            datos.get("confirmar", ""),
            datos.get("rol", ""),
            datos.get("cargo", ""),
        )
    except PermissionError as error:
        return jsonify({"error": str(error)}), 403
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(usuario), 201