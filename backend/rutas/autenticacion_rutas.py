from flask import Blueprint, request, jsonify
from servicios.autenticacion_servicio import AutenticacionServicio

autenticacion_bp = Blueprint("autenticacion", __name__)
servicio = AutenticacionServicio()




@autenticacion_bp.route("/api/login", methods=["POST"])
def login():
    datos = request.get_json() or {}
    correo = datos.get("correo", "")
    clave = datos.get("clave", "")
    rol = datos.get("rol", "")

    usuario = servicio.iniciar_sesion(correo, clave, rol)
    if usuario is None:
        return jsonify({"error": "Credenciales incorrectas"}), 401
    return jsonify({"usuario": usuario})

@autenticacion_bp.route("/api/registro", methods=["POST"])
def registro():
    datos = request.get_json() or {}
    try:
        usuario = servicio.registrar_cliente(
            datos.get("nombre", ""),
            datos.get("correo", ""),
            datos.get("telefono", ""),
            datos.get("clave", ""),
            datos.get("confirmar", ""),
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"usuario": usuario}), 201