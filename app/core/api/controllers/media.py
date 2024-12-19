from datetime import timedelta
from flask import request
from sqlalchemy.exc import ( IntegrityError, DataError, DatabaseError, InvalidRequestError, OperationalError )
from werkzeug.exceptions import UnsupportedMediaType
from flask_jwt_extended import create_access_token
from flask_jwt_extended.exceptions import JWTDecodeError
from jwt import ExpiredSignatureError, DecodeError
from email_validator import validate_email, EmailNotValidError, ValidatedEmail

from ....extensions import db
from ....models import Role, RoleNames, AppUser, Address, Profile
from ....utils.helpers.loggers import console_log, log_exception
from ....utils.helpers.http_response import error_response, success_response
from ....utils.helpers.users import get_app_user


class MediaController:
    @staticmethod
    def get_media():
        try:
            pass
        except Exception as e:
            log_exception("An exception occurred adding a project:", e)
            return error_response("An unexpected error occurred", 500)
    
    @staticmethod
    def add_media():
        try:
            pass
        except Exception as e:
            log_exception("An exception occurred adding a project:", e)
            return error_response("An unexpected error occurred", 500)
    
    @staticmethod
    def get_media(media_id):
        try:
            pass
        except Exception as e:
            log_exception("An exception occurred adding a project:", e)
            return error_response("An unexpected error occurred", 500)
    
    @staticmethod
    def edit_media(media_id):
        try:
            pass
        except Exception as e:
            log_exception("An exception occurred adding a project:", e)
            return error_response("An unexpected error occurred", 500)
    
    @staticmethod
    def delete_media(media_id):
        try:
            pass
        except Exception as e:
            log_exception("An exception occurred adding a project:", e)
            return error_response("An unexpected error occurred", 500)