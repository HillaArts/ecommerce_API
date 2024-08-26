from flasgger import Swagger

def setup_swagger(app):
    """
    Set up Swagger UI for the Flask application.
    
    Args:
        app (Flask): The Flask application instance.
    """
    Swagger(app, template_file='app/static/swagger.yaml')