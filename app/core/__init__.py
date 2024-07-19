from flask import Flask

def register_all_blueprints(app: Flask) -> None:
    
    from .routes.base import base_bp
    app.register_blueprint(base_bp)
    
    from .routes.api import api_bp
    app.register_blueprint(api_bp)
    
    from .routes.admin_api import admin_api_bp
    app.register_blueprint(admin_api_bp)
    
    from .error_handlers import errors_bp
    app.register_blueprint(errors_bp)
    
    # Swagger setup
    from flask_swagger_ui import get_swaggerui_blueprint

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
