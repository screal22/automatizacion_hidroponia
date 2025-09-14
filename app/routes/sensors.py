from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import EstadoBomba

sensors_bp = Blueprint("sensors", __name__)

@sensors_bp.route("/add_pump_data", methods=["POST"])
def add_pump_data():
    data = request.get_json()
    if not data or "estado" not in data or "tiempo_llenado" not in data:
        return jsonify({"error": "Faltan datos"}), 400

    new_entry = EstadoBomba(
        estado=data["estado"],
        tiempo_llenado=data["tiempo_llenado"]
    )
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({"message": "Datos guardados correctamente", "id": new_entry.id}), 201