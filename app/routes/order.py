from flask import Blueprint, request, jsonify
from app.models.order import Order
from app.models.orderproduct import OrderProduct
from app.models.product import Product  
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.decorators import client_required

bp = Blueprint('order', __name__, url_prefix='/orders')

@bp.route('/', methods=['GET', 'POST'])
@jwt_required()
@client_required
def manage_orders():
    user_id = get_jwt_identity()['id']

    if request.method == 'GET':
        orders = Order.query.filter_by(user_id=user_id).all()
        return jsonify([order.to_dict() for order in orders]), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        products_data = data.get('products')

        order = Order(user_id=user_id)
        db.session.add(order)
        db.session.commit()

        total_price = 0
        for product_data in products_data:
            product_id = product_data['product_id']
            quantity = product_data['quantity']
            product = Product.query.get(product_id)
            if product:
                order_product = OrderProduct(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price_at_order=product.price
                )
                db.session.add(order_product)
                total_price += product.price * quantity

        order.total_price = total_price
        db.session.commit()

        return jsonify({"message": "Order created successfully"}), 201

@bp.route('/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
@client_required
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