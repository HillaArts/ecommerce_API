from flask import Blueprint, request, jsonify
from app.models.order import Order
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('order', __name__, url_prefix='/orders')

@bp.route('/', methods=['GET', 'POST'])
@jwt_required()
def manage_orders():
    user_id = get_jwt_identity()['id']

    if request.method == 'GET':
        orders = Order.query.filter_by(user_id=user_id).all()
        return jsonify([order.to_dict() for order in orders]), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        total_price = data.get('total_price')

        order = Order(user_id=user_id, total_price=total_price)
        db.session.add(order)
        db.session.commit()

        return jsonify({"message": "Order created successfully"}), 201

@bp.route('/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
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
