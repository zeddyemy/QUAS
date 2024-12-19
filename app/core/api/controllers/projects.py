from datetime import timedelta
from flask import request
from sqlalchemy.exc import ( IntegrityError, DataError, DatabaseError, InvalidRequestError, OperationalError )
from werkzeug.exceptions import UnsupportedMediaType
from flask_jwt_extended import create_access_token
from flask_jwt_extended.exceptions import JWTDecodeError
from jwt import ExpiredSignatureError, DecodeError
from email_validator import validate_email, EmailNotValidError, ValidatedEmail

from ....extensions import db
from ....models import AppUser, Project
from ....utils.helpers.users import get_current_user
from ....utils.helpers.loggers import console_log, log_exception
from ....utils.helpers.http_response import error_response, success_response
from ....utils.helpers.users import get_app_user
from ....utils.helpers.export_xl import export_to_excel


class ProjectsController:
    @staticmethod
    def get_projects():
        try:
            current_user = get_current_user()
            if not current_user:
                return error_response("Unauthorized", 401)
            
            page = request.args.get("page", 1, type=int)
            per_page = request.args.get("per_page", 5, type=int)
            search_term = request.args.get("search")
            
            query = Project.query.order_by(Project.created_at.desc())
            query = Project.add_search_filters(query, search_term)
            
            if request.args.get('export', '').lower() == "excel":
                filename = "trips"
                return export_to_excel(query.all(), filename)
            
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            
            projects: list[Project] = pagination.items
            current_projects = [project.to_dict() for project in projects]
            extra_data = {
                "total": pagination.total,
                "projects": current_projects,
                "current_page": pagination.page,
                "total_pages": pagination.pages,
            }
            
            api_response = success_response("Projects fetched successfully", 200, extra_data)
            
        except Exception as e:
            log_exception("An exception occurred adding a project:", e)
            api_response = error_response("An unexpected error occurred", 500)
        
        return api_response
    
    @staticmethod
    def add_project():
        try:
            current_user = get_current_user()
            if not current_user:
                return error_response("Unauthorized", 401)
            
            data = request.get_json()
            
            name = data.get('name')
            description = data.get('description')
            
            if not data or not name:
                return error_response("Project name is required.", 400)
            
            new_project = Project(
                name=name,
                description=description
            )
            db.session.add(new_project)
            db.session.commit()
            
            extra_data = {"project": new_project.to_dict()}
            
            api_response = success_response("Project added successfully", 200, extra_data)
        except (DataError, DatabaseError) as e:
            log_exception('Database error occurred adding new project', e)
            api_response = error_response('Error interacting to the database.', 500)
        except Exception as e:
            log_exception("An exception occurred adding a project:", e)
            api_response = error_response("An unexpected error occurred", 500)
        finally:
            db.session.close()
        
        return api_response
    
    @staticmethod
    def get_project(project_id):
        try:
            pass
        except Exception as e:
            log_exception("An exception occurred adding a project:", e)
            return error_response("An unexpected error occurred", 500)
    
    @staticmethod
    def edit_project(project_id):
        try:
            pass
        except Exception as e:
            log_exception("An exception occurred adding a project:", e)
            api_response = error_response("An unexpected error occurred", 500)
        finally:
            db.session.close()
        
        return api_response
    
    @staticmethod
    def delete_project(project_id):
        try:
            pass
        except Exception as e:
            log_exception("An exception occurred adding a project:", e)
            return error_response("An unexpected error occurred", 500)