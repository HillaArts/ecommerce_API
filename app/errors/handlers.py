from flask import jsonify

def bad_request_error(error):
    """
    Handle 400 Bad Request errors.
    
    Args:
        error (Exception): The exception that triggered the error handler.
    
    Returns:
        Response: A JSON response with the error message and a 400 status code.
    """
    return jsonify({"error": "Bad request", "message": str(error)}), 400

def not_found_error(error):
    """
    Handle 404 Not Found errors.
    
    Args:
        error (Exception): The exception that triggered the error handler.
    
    Returns:
        Response: A JSON response with the error message and a 404 status code.
    """
    return jsonify({"error": "Not found", "message": str(error)}), 404

def internal_error(error):
    """
    Handle 500 Internal Server Error errors.
    
    Args:
        error (Exception): The exception that triggered the error handler.
    
    Returns:
        Response: A JSON response with the error message and a 500 status code.
    """
    return jsonify({"error": "Internal server error", "message": str(error)}), 500