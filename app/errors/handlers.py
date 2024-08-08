# app/errors/handlers.py
from flask import jsonify

def bad_request_error(error):
    return jsonify({"error": "Bad request", "message": str(error)}), 400

def not_found_error(error):
    return jsonify({"error": "Not found", "message": str(error)}), 404

def internal_error(error):
    return jsonify({"error": "Internal server error", "message": str(error)}), 500
