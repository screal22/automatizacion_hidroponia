from flask import Flask
from .extensions import db, migrate
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints
    from .routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix="/users")

    @app.route("/")
    def home():
        return {"message": "Hola desde Flask en DigitalOcean 🚀"}

    return app
