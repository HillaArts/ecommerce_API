from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.models.order import Order
from app.models.user import User
from app.extensions import db, jwt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.decorators import admin_required, client_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Initialize CORS for this Blueprint
CORS(auth_bp)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Returns:
        JSON response with a success message or an error message.
    """
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

@auth_bp.route('/register/admin', methods=['POST'])
def register_admin():
    """
    Register a new admin user.
    
    Returns:
        JSON response with a success message or an error message.
    """
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(username=username, email=email, role='admin')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Admin created successfully"}), 201

@auth_bp.route('/register/client', methods=['POST'])
def register_client():
    """
    Register a new client user.
    
    Returns:
        JSON response with a success message or an error message.
    """
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(username=username, email=email, role='client')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Client created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Log in a user.
    
    Returns:
        JSON response with an access token or an error message.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity={'id': user.id, 'username': user.username})
    return jsonify(access_token=access_token), 200

@auth_bp.route('/login/admin', methods=['POST'])
def login_admin():
    """
    Log in an admin user.
    
    Returns:
        JSON response with an access token or an error message.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    if user.role != 'admin':
        return jsonify({"error": "Access forbidden: Admins only"}), 403

    access_token = create_access_token(identity={'id': user.id, 'username': user.username})
    return jsonify(access_token=access_token), 200

@auth_bp.route('/login/client', methods=['POST'])
def login_client():
    """
    Log in a client user.
    
    Returns:
        JSON response with an access token or an error message.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    if user.role != 'client':
        return jsonify({"error": "Access forbidden: Clients only"}), 403

    access_token = create_access_token(identity={'id': user.id, 'username': user.username})
    return jsonify(access_token=access_token), 200

@auth_bp.route('/delete/admin/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_admin(user_id):
    """
    Delete an admin user.
    
    Args:
        user_id (int): The ID of the user to delete.
    
    Returns:
        JSON response with a success message or an error message.
    """
    current_user = get_jwt_identity()

    # Logging the current user and the user to delete for debugging
    print(f"Current User: {current_user}")
    print(f"User ID to delete: {user_id}")

    # Fetch the user to delete from the database
    user_to_delete = User.query.get(user_id)
    
    # Check if the user to delete exists
    if not user_to_delete:
        return jsonify({"error": "User not found"}), 404

    # Check if the user to delete is an admin and if it's the same as the current user
    if user_to_delete.role == 'admin' and current_user['id'] != user_id:
        return jsonify({"error": "Cannot delete another admin"}), 403
    
    if user_to_delete.id is None:
        return jsonify({"error": "User ID is null, cannot delete"}), 400

    try:
        # Delete the user
        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify({"message": "User account deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()  # Rollback in case of any errors
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/delete/client/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_client(user_id):
    """
    Delete a client user.
    
    Args:
        user_id (int): The ID of the user to delete.
    
    Returns:
        JSON response with a success message or an error message.
    """
    # Log user ID for debugging
    print(f"Attempting to delete client with user_id: {user_id}")

    # Retrieve the user to delete
    user_to_delete = User.query.get(user_id)
    if not user_to_delete:
        return jsonify({"error": "User not found"}), 404

    # Optionally, handle related records if necessary
    # Example: Update orders to remove the user_id or handle cascading deletes
    orders = Order.query.filter_by(user_id=user_id).all()
    for order in orders:
        order.user_id = None  # Or handle as needed
        db.session.add(order)

    try:
        # Delete the user
        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify({"message": "Client account deleted successfully"}), 200
    except Exception as e:
        # Rollback in case of an error
        db.session.rollback()
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while deleting the user"}), 500

@auth_bp.route('/users/admin', methods=['GET'])
@jwt_required()
@admin_required
def list_admin_users():
    """
    List all admin users.
    
    Returns:
        JSON response with a list of admin users.
    """
    identity = get_jwt_identity()
    current_user = User.query.get(identity['id'])
    if current_user.role != 'admin':
        return jsonify({"error": "Access forbidden: Admins only"}), 403

    admins = User.query.filter_by(role='admin').all()
    result = [
        {
            "id": admin.id,
            "username": admin.username,
            "email": admin.email
        }
        for admin in admins
    ]
    return jsonify(result), 200

@auth_bp.route('/users/client', methods=['GET'])
@jwt_required()
@admin_required
def list_client_users():
    """
    List all client users.
    
    Returns:
        JSON response with a list of client users.
    """
    identity = get_jwt_identity()
    current_user = User.query.get(identity['id'])
    if current_user.role != 'admin':
        return jsonify({"error": "Access forbidden: Admins only"}), 403

    clients = User.query.filter_by(role='client').all()
    result = [
        {
            "id": client.id,
            "username": client.username,
            "email": client.email
        }
        for client in clients
    ]
    return jsonify(result), 200