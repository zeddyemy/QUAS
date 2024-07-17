'''
This package contains the main routes for the QUAS Flask application.

A Flask blueprint named 'main' is created to group these routes.

@author: Emmanuel Olowu
@link: https://github.com/zeddyemy
@package: QUAS
'''
from flask import Blueprint, render_template

base_bp: Blueprint = Blueprint('base', __name__)

@base_bp.route("/", methods=['GET'])
def index():
    return render_template('api/index.jinja-html')