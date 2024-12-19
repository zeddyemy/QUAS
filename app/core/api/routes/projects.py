from flask import request
from flask_jwt_extended import jwt_required

from . import api_bp
from ..controllers import ProjectsController


@api_bp.route("/projects", methods=["GET", "POST"])
def projects():
    if request.method == "GET":
        return ProjectsController.get_projects()
    elif request.method == "POST":
        return ProjectsController.add_project()


@api_bp.route("/projects/<project_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def manage_project(project_id):
    if request.method == "GET":
        return ProjectsController.get_task(project_id)
    if request.method == "PUT":
        return ProjectsController.edit_task(project_id)
    elif request.method == "DELETE":
        return ProjectsController.delete_task(project_id)