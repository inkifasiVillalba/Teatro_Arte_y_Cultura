from flask import Blueprint, jsonify
from servicios.dashboard_servicio import DashboardServicio

dashboard_bp = Blueprint("dashboard", __name__)
servicio = DashboardServicio()


@dashboard_bp.route("/api/dashboard")
def dashboard():
    return jsonify(servicio.resumen())
