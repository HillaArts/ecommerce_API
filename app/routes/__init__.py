from flask import Blueprint
from app.routes.auth import auth_bp
from .product import bp as product_bp
from .order import bp as order_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    
