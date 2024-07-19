import json
from sqlalchemy.exc import ( IntegrityError, DataError, DatabaseError, InvalidRequestError, OperationalError )

from . import errors_bp

from ...utils.helpers.loggers import log_exception
from ...utils.helpers.http_response import error_response


@errors_bp.app_errorhandler(OperationalError)
def operational_error(error):
    log_exception("SQLalchemy Database Error", error)
    return error_response('Error interacting to the database.', 500)

@errors_bp.app_errorhandler(DataError)
def data_error(error):
    log_exception("SQLalchemy Database Error", error)
    return error_response('Error interacting to the database.', 500)

@errors_bp.app_errorhandler(DatabaseError)
def database_error(error):
    log_exception("SQLalchemy Database Error", error)
    return error_response('Error interacting to the database.', 500)

@errors_bp.app_errorhandler(IntegrityError)
def integrity_error(error):
    log_exception("SQLalchemy Database Error", error)
    return error_response('Error interacting to the database.', 500)

@errors_bp.app_errorhandler(InvalidRequestError)
def invalid_request_error(error):
    log_exception("SQLalchemy Database Error", error)
    return error_response('Error interacting to the database.', 500)

