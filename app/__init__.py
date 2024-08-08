from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from app.models import db
from app.errors import register_error_handlers
from app.routes import bp
from app.docs import setup_swagger

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(bp)
    setup_swagger(app)

    with app.app_context():
        db.create_all()
        register_error_handlers(app)

    return app