from flask import request
from flask_jwt_extended import jwt_required

from . import api_bp
from ..controllers import AnnotationsController


@api_bp.route("/annotations", methods=["GET", "POST"])
def annotations():
    if request.method == "GET":
        return AnnotationsController.get_annotations()
    elif request.method == "POST":
        return AnnotationsController.add_annotation()


@api_bp.route("/projects/<annotation_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def manage_annotation(annotation_id):
    if request.method == "GET":
        return AnnotationsController.get_annotation(annotation_id)
    if request.method == "PUT":
        return AnnotationsController.edit_annotation(annotation_id)
    elif request.method == "DELETE":
        return AnnotationsController.delete_annotation(annotation_id)