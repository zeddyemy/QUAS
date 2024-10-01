from flask import Blueprint, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


cpanel_bp = Blueprint('cpanel', __name__, url_prefix="/cpanel")

from . import auth
