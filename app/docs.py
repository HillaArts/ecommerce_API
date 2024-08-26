from flasgger import Swagger

def setup_swagger(app):
    """
    Set up Swagger for the Flask application.
    
    Args:
        app (Flask): The Flask application instance.
    """
    Swagger(app, template_file='static/swagger.yaml')