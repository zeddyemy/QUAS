'''
This module initializes the extensions used in the QUAS Flask application.

It sets up SQLAlchemy, Flask-Mail, and Celery with the configurations defined in the Config class.

@author: Emmanuel Olowu
@link: https://github.com/zeddyemy
'''
# from flask_restx import Api

# api = Api(version=1.0, doc='/swagger/doc')

from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, UserMixin, current_user

from config import Config

mail = Mail()
cors = CORS()
db = SQLAlchemy()
migration = Migrate()
jwt_extended = JWTManager()
limiter = Limiter(key_func=get_remote_address)
login_manager = LoginManager()

def initialize_extensions(app: Flask):
    """
    initializes the extensions used in the Flask application.
    
    Return: None
    """
    
    db.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    migration.init_app(app, db=db)
    jwt_extended.init_app(app) # Setup the Flask-JWT-Extended extension
    
    login_manager.init_app(app)
    login_manager.login_view = 'cpanel.login'
    
    from .models import AppUser
    @login_manager.user_loader
    def load_user(user_id):
        return AppUser.query.get(int(user_id))
    
    # Set up CORS. Allow '*' for origins.
    cors.init_app(app=app, resources={r"/*": {"origins": Config.CLIENT_ORIGINS}}, supports_credentials=True)