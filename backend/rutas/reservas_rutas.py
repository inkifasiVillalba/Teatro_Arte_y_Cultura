from flask import Blueprint, request, jsonify
from servicios.reserva_servicio import ReservaServicio

reservas_bp = Blueprint("reservas", __name__)
servicio = ReservaServicio()


@reservas_bp.route("/api/reservar", methods=["POST"])
def reservar():
    d = request.get_json() or {}
    try:
        resultado = servicio.reservar(
            d.get("id_cliente"), d.get("id_funcion"),
            d.get("asientos", []), d.get("precio", 0),
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(resultado), 201


@reservas_bp.route("/api/reservas/pendientes")
def pendientes():
    return jsonify(servicio.pendientes())


@reservas_bp.route("/api/reservas/<int:id_reserva>/cobrar", methods=["POST"])
def cobrar(id_reserva):
    d = request.get_json() or {}
    try:
        resultado = servicio.cobrar(id_reserva, d.get("id_empleado"), d.get("metodo", ""))
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(resultado)


@reservas_bp.route("/api/reservas/<int:id_reserva>/cancelar", methods=["POST"])
def cancelar(id_reserva):
    try:
        servicio.cancelar(id_reserva)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"mensaje": "Reserva cancelada"})