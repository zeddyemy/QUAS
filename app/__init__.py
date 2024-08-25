from flask import Flask
from flask_cors import CORS

from .extensions import initialize_extensions
from config import Config, config_by_name, configure_logging
from .utils import set_access_control_allows
from .models import create_roles


def create_app(config_name=Config.ENV):
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
    
    # Set up CORS. Allow '*' for origins.
    cors = CORS(app, resources={r"/*": {"origins": Config.CLIENT_ORIGINS}}, supports_credentials=True)

    # Use the after_request decorator to set Access-Control-Allow
    app.after_request(set_access_control_allows)
    
    
    # Configure logging
    configure_logging(app)
    
    
    # Register blueprints
    from .core import register_all_blueprints
    register_all_blueprints(app)
    
    # with app.app_context():
    #     create_roles()  # Create roles for trendit3
    
    return app