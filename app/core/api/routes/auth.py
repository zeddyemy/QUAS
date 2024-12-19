'''
This module defines the routes for authentication operations in the QUAS Flask application.

It includes routes for signing up, verifying email, logging in, verifying 2FA, forgetting password, and resetting password.

@author: Emmanuel Olowu
@link: https://github.com/zeddyemy
@package: QUAS
'''
from flask import request
from flask_jwt_extended import jwt_required

from . import api_bp
from ..controllers import AuthController


# REGISTRATION ENDPOINTS
@api_bp.route("/signup", methods=['POST'])
def sign_up():
    return AuthController.sign_up()

# AUTHENTICATION ENDPOINTS
@api_bp.route("/login", methods=['POST'])
def login():
    return AuthController.login()