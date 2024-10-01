import json


from . import errors_bp
from ...utils.helpers.loggers import log_exception
from ...utils.helpers.http_response import error_response

@errors_bp.app_errorhandler(json.JSONDecodeError)
def json_decode_error(error):
    log_exception("JSONDecodeError", error)
    return error_response(f"Invalid or no JSON object.", 400)

@errors_bp.app_errorhandler(Exception)
def database_Error(error):
    log_exception("Regular Exception", error)
    return error_response('An unexpected error. Our developers are already looking into it.', 500)