from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.user import User

def admin_required(fn):
    """
    Decorator to ensure that the user is an admin.
    
    Args:
        fn (function): The function to be decorated.
    
    Returns:
        function: The wrapped function.
    """
    @wraps(fn)
    @jwt_required()  # Ensure JWT is required
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if not isinstance(identity, dict):
            return jsonify({'error': 'Invalid token format'}), 400

        current_user_id = identity.get('id')
        if current_user_id is None:
            return jsonify({'error': 'User ID not found in token'}), 400
        
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        if current_user.role != 'admin':
            return jsonify({'error': 'Access forbidden: Admins only'}), 403
        
        return fn(*args, **kwargs)
    return wrapper

def client_required(fn):
    """
    Decorator to ensure that the user is a client.
    
    Args:
        fn (function): The function to be decorated.
    
    Returns:
        function: The wrapped function.
    """
    @wraps(fn)
    @jwt_required()  # Ensure JWT is required
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if not isinstance(identity, dict):
            return jsonify({'error': 'Invalid token format'}), 400
        
        current_user_id = identity.get('id')
        if current_user_id is None:
            return jsonify({'error': 'User ID not found in token'}), 400
        
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        if current_user.role != 'client':
            return jsonify({'error': 'Access forbidden: Clients only'}), 403
        
        return fn(*args, **kwargs)
    return wrapper