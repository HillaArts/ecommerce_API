from flasgger import Swagger

def setup_swagger(app):
    """
    Setup Swagger UI for the Flask application.
    """
    Swagger(app, template_file='app/static/swagger.yaml')

