from flask import Blueprint, request, jsonify
from servicios.producto_servicio import ProductoServicio

productos_bp = Blueprint("productos", __name__)
servicio = ProductoServicio()


@productos_bp.route("/api/productos")
def listar_productos():
    return jsonify(servicio.listar())


@productos_bp.route("/api/productos/vender", methods=["POST"])
def vender_producto():
    datos = request.get_json() or {}
    try:
        resultado = servicio.vender(datos.get("id_producto"), datos.get("cantidad"))
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(resultado)

@productos_bp.route("/api/productos/ajustar", methods=["POST"])
def ajustar_producto():
    datos = request.get_json() or {}
    try:
        resultado = servicio.ajustar_stock(datos.get("id_producto"), datos.get("cambio", 0))
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(resultado)