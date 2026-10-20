from flask import Blueprint, jsonify
from repositorios.historial_repositorio import HistorialRepositorio

historial_bp = Blueprint("historial", __name__)
repositorio = HistorialRepositorio()


@historial_bp.route("/api/clientes/<int:id_cliente>/historial")
def historial(id_cliente):
    entradas = repositorio.entradas_de_cliente(id_cliente)
    reservas = repositorio.reservas_de_cliente(id_cliente)
    for e in entradas:
        e["fecha_hora"] = e["fecha_hora"].strftime("%Y-%m-%d %H:%M")
        e["precio"] = float(e["precio"])
    for r in reservas:
        r["fecha_hora"] = r["fecha_hora"].strftime("%Y-%m-%d %H:%M")
        r["total"] = float(r["total"])
    return jsonify({"entradas": entradas, "reservas": reservas})