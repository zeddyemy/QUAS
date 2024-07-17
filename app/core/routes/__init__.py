from flask import Flask
from .admin_api import admin_api_bp
from .api import api_bp
from .base import base_bp

def register_all_blueprints(app: Flask) -> None:
    app.register_blueprint(base_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_api_bp)
    
    # Swagger setup
    from flask_swagger_ui import get_swaggerui_blueprint

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)