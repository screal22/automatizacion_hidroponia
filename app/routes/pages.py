from flask import Blueprint, render_template
from ..models import EstadoBomba

pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/")
def home():
    # Traer todos los registros de la base de datos
    datos = EstadoBomba.query.all()
    return render_template("home.html", datos=datos)
