from flask import Blueprint, request, jsonify
from servicios.venta_servicio import VentaServicio

ventas_bp = Blueprint("ventas", __name__)
servicio = VentaServicio()


@ventas_bp.route("/api/comprar", methods=["POST"])
def comprar():
    datos = request.get_json() or {}
    try:
        resultado = servicio.comprar(
            datos.get("id_cliente"),
            datos.get("id_funcion"),
            datos.get("asientos", []),
            datos.get("precio", 0),
            datos.get("metodo", ""),
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(resultado), 201