from flask import Blueprint, request, jsonify
from app.models.product import Product
from app.extensions import db
from flask_jwt_extended import jwt_required

bp = Blueprint('product', __name__, url_prefix='/products')

@bp.route('/', methods=['GET', 'POST'])
@jwt_required()
def manage_products():
    if request.method == 'GET':
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        stock = data.get('stock', 0)

        product = Product(name=name, description=description, price=price, stock=stock)
        db.session.add(product)
        db.session.commit()

        return jsonify({"message": "Product created successfully"}), 201

@bp.route('/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'GET':
        return jsonify(product.to_dict()), 200
    
    elif request.method == 'PUT':
        data = request.get_json()
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.stock = data.get('stock', product.stock)
        db.session.commit()

        return jsonify({"message": "Product updated successfully"}), 200
    
    elif request.method == 'DELETE':
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
