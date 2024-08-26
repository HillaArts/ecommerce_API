"""
This module initializes the Flask application and its extensions.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.extensions import db, migrate
from app.errors import register_error_handlers
from app.routes import register_blueprints
from app.docs import setup_swagger
from app.config import DevelopmentConfig, TestingConfig, ProductionConfig

jwt = JWTManager()

def create_app(config_class=DevelopmentConfig):
    """
    Create and configure an instance of the Flask application.
    
    Args:
        config_class (class): The configuration class to use.
    
    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    register_blueprints(app)  # Ensure this function is defined in `app/routes/__init__.py`
    setup_swagger(app)

    with app.app_context():
        db.create_all()  # Create database tables
        register_error_handlers(app)  # Register custom error handlers

    return app