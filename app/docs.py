from flasgger import Swagger

def setup_swagger(app):
    Swagger(app, template_file='static/swagger.yaml')
