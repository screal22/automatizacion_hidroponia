from flask import Flask
from .extensions import db, migrate
from .config import Config
from app.mqtt_listener import start_mqtt_listener

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Importar modelos aquí
    from .models import User, EstadoBomba

    # Registrar blueprints
    from .routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix="/users")

    from .routes.sensors import sensors_bp
    app.register_blueprint(sensors_bp, url_prefix="/sensors")

    from .routes.pages import pages_bp
    app.register_blueprint(pages_bp)

    # @app.route("/")
    # def home():
    #     return {"message": "Hola desde Flask en DigitalOcean 🚀"}
    
    with app.app_context():
        # Iniciar el listener MQTT
        start_mqtt_listener(app)

    return app
