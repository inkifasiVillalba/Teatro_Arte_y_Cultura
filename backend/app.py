from flask import Flask, jsonify
from flask_cors import CORS
from rutas.autenticacion_rutas import autenticacion_bp
from rutas.obras_rutas import obras_bp
from rutas.funciones_rutas import funciones_bp
from rutas.ventas_rutas import ventas_bp
from rutas.entradas_rutas import entradas_bp
from rutas.productos_rutas import productos_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(autenticacion_bp)
app.register_blueprint(obras_bp)  
app.register_blueprint(funciones_bp)   
app.register_blueprint(ventas_bp)
app.register_blueprint(entradas_bp)
app.register_blueprint(productos_bp)

@app.route("/api/salud")
def salud():
    return jsonify({"mensaje": "Servidor del Teatro Arte y Cultura funcionando"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)


