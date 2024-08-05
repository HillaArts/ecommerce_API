# app/routes.py
from flask import Blueprint, request, jsonify
from .models import Product, User, Order, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp = Blueprint('api', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity={'id': user.id, 'username': user.username})
    return jsonify(access_token=access_token), 200

@bp.route('/products', methods=['GET', 'POST'])
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

@bp.route('/products/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
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

@bp.route('/orders', methods=['GET', 'POST'])
@jwt_required()
def manage_orders():
    if request.method == 'GET':
        user_id = get_jwt_identity()['id']
        orders = Order.query.filter_by(user_id=user_id).all()
        return jsonify([order.to_dict() for order in orders]), 200
    
    elif request.method == 'POST':
        user_id = get_jwt_identity()['id']
        data = request.get_json()
        total_price = data.get('total_price')

        order = Order(user_id=user_id, total_price=total_price)
        db.session.add(order)
        db.session.commit()

        return jsonify({"message": "Order created successfully"}), 201

@bp.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)

    if request.method == 'GET':
        return jsonify(order.to_dict()), 200

    elif request.method == 'PUT':
        data = request.get_json()
        order.status = data.get('status', order.status)
        db.session.commit()

        return jsonify({"message": "Order updated successfully"}), 200

    elif request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted successfully"}), 200
