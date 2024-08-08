from flask import Flask
from .handlers import bad_request_error, not_found_error, internal_error

def register_error_handlers(app: Flask):
    app.register_error_handler(400, bad_request_error)
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_error)
