'''
This package contains the admin API routes for the Flask application.
It includes routes for admin authentication, stats, user management, and settings.

A Flask blueprint named 'api_admin' is created to group these routes, and it is registered under the '/api/admin' URL prefix.

@author: Emmanuel Olowu
@link: https://github.com/zeddyemy
'''
from flask import Blueprint

admin_api_bp: Blueprint = Blueprint('api_admin', __name__, url_prefix='/api/admin')

# from . import auth, task_performance, dashboard, tasks, users, transactions, pricing, social_profile, wallet, stats

@admin_api_bp.route('/')
def index():
    return 'Admin API routes'