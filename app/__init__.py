from flask import Flask

from .extensions import initialize_extensions
from config import Config, config_by_name, configure_logging
from .models import create_db_defaults
from .core.cpanel.setup import setup_flask_admin
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
    
    initialize_extensions(app) # Initialize Flask extensions
    
    setup_flask_admin(app) # Set up flask admin

    register_hooks(app=app) # Register before and after request hooks
    
    configure_logging(app) # Configure logging
    
    
    # Register blueprints
    from .blueprints import register_all_blueprints
    register_all_blueprints(app)
    
    # create defaults
    if create_defaults:
        create_db_defaults(app)
    
    return app