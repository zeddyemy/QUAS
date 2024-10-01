import json
from flask import Blueprint, Flask

from ..routes import api_bp
from ....utils.helpers.loggers import log_exception, console_log
from ....utils.helpers.http_response import error_response


# def register_error_handlers(app: Flask) -> None:
#     """ Register error handlers"""
    
#     app.errorhandler(OperationalError)(operational_error)


@api_bp.app_errorhandler(json.JSONDecodeError)
def json_decode_error(error):
    log_exception("JSONDecodeError", error)
    return error_response(f"Invalid or no JSON object.", 400)

@api_bp.app_errorhandler(Exception)
def database_Error(error):
    log_exception("Regular Exception", error)
    return error_response('An unexpected error. Our developers are already looking into it.', 500)