'''
This module defines the routes for authentication operations in the Flask application.

It includes routes for signing up, verifying email, logging in, verifying 2FA, forgetting password, and resetting password.

@author: Emmanuel Olowu
@link: https://github.com/zeddyemy
@package: label_box
'''
from flask import request
from flask_jwt_extended import jwt_required

from . import api_bp
from ..controllers import TasksController


@api_bp.route("/tasks", methods=["GET", "POST"])
def tasks():
    if request.method == "GET":
        return TasksController.get_tasks()
    elif request.method == "POST":
        return TasksController.add_task()


@api_bp.route("/tasks/<task_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def manage_task(task_id):
    if request.method == "GET":
        return TasksController.get_task(task_id)
    if request.method == "PUT":
        return TasksController.edit_task(task_id)
    elif request.method == "DELETE":
        return TasksController.delete_task(task_id)