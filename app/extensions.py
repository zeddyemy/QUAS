'''
This module initializes the extensions used in the QUAS Flask application.

It sets up SQLAlchemy, Flask-Mail, and Celery with the configurations defined in the Config class.

@author: Emmanuel Olowu
@link: https://github.com/zeddyemy
@package: QUAS
'''
# from flask_restx import Api

# api = Api(version=1.0, doc='/swagger/doc')

from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_limiter.util import get_remote_address

mail = Mail()
db = SQLAlchemy()
migration = Migrate()
jwt_extended = JWTManager()

def initialize_extensions(app: Flask):
    db.init_app(app)
    mail.init_app(app) # Initialize Flask-Mail
    jwt = jwt_extended.init_app(app) # Setup the Flask-JWT-Extended extension
    migrate = migration.init_app(app, db=db)