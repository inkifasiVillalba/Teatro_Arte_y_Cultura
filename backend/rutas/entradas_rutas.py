from flask import Blueprint, request, jsonify
from servicios.entrada_servicio import EntradaServicio

entradas_bp = Blueprint("entradas", __name__)
servicio = EntradaServicio()


@entradas_bp.route("/api/entradas/validar", methods=["POST"])
def validar_entrada():
    datos = request.get_json() or {}
    try:
        resultado = servicio.validar(datos.get("codigo", ""))
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(resultado)