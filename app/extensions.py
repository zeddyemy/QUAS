'''
This module initializes the extensions used in the QUAS Flask application.

It sets up SQLAlchemy, Flask-Mail, and Celery with the configurations defined in the Config class.

@author: Emmanuel Olowu
@link: https://github.com/zeddyemy
@package: QUAS
'''
# from flask_restx import Api

# api = Api(version=1.0, doc='/swagger/doc')

from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

mail = Mail()
db = SQLAlchemy()
migration = Migrate()
jwt_extended = JWTManager()
limiter = Limiter(key_func=get_remote_address)