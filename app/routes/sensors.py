from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import EstadoBomba
from datetime import datetime

sensors_bp = Blueprint("sensors", __name__)

@sensors_bp.route("/add_pump_data", methods=["POST"])
def add_pump_data():
    data = request.get_json()
    if not data or "estado" not in data or "tiempo_llenado" not in data:
        return jsonify({"error": "Faltan datos"}), 400
    
    estado = data["estado"]
    tiempo_llenado = data["tiempo_llenado"]

    # Si el estado es "Apagado manual", calcular tiempo de llenado desde el último "Encendido manual"
    if estado == "Apagado manual":
        ultimo_encendido = EstadoBomba.query.order_by(EstadoBomba.fecha_creacion.desc()).first()
        if ultimo_encendido:
            tiempo_llenado = (datetime.now() - ultimo_encendido.fecha_creacion).total_seconds()

    new_entry = EstadoBomba(
        estado=estado,
        tiempo_llenado=tiempo_llenado
    )
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({"message": "Datos guardados correctamente", "id": new_entry.id}), 201

@sensors_bp.route("/last_pump_state", methods=["GET"])
def last_pump_state():
    # Consulta el último registro ordenando por fecha de creación descendente
    last_entry = EstadoBomba.query.order_by(EstadoBomba.fecha_creacion.desc()).first()
    
    if not last_entry:
        return jsonify({"error": "No hay registros"}), 404

    # Retorna los datos en formato JSON
    return jsonify({
        "id": last_entry.id,
        "estado": last_entry.estado,
        "tiempo_llenado": last_entry.tiempo_llenado,
        "fecha_creacion": last_entry.fecha_creacion
    }), 200