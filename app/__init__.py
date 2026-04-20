from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Registrar los blueprints
    from app.routes.salones import salones_bp
    from app.routes.alumnos import alumnos_bp
    from app.routes.calificaciones import calificaciones_bp

    app.register_blueprint(salones_bp)
    app.register_blueprint(alumnos_bp)
    app.register_blueprint(calificaciones_bp)

    return app
