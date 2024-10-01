from flask import Flask

from .extensions import initialize_extensions
from config import Config, config_by_name, configure_logging
from .models import create_roles
from .utils.hooks import register_hooks


def create_app(config_name=Config.ENV, create_defaults=True):
    '''
    Creates and configures the Flask application instance.

    Args:
        config_name: The configuration class to use (Defaults to Config).

    Returns:
        The Flask application instance.
    '''
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # Initialize Flask extensions
    initialize_extensions(app)

    # Register before and after request hooks
    register_hooks(app=app)
    
    
    # Configure logging
    configure_logging(app)
    
    
    # Register blueprints
    from .blueprints import register_all_blueprints
    register_all_blueprints(app)
    
    if create_defaults:
        with app.app_context():
            create_roles()
    
    return app