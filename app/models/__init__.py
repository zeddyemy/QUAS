'''
This package contains the database models for the Flask application.

It includes models for AppUser, Role, etc. Each model corresponds to a table in the database.

@author Emmanuel Olowu
@link: https://github.com/zeddyemy
'''
from flask import Flask

from .media import Media
from .user import AppUser, Profile, Address, create_default_super_admin
from .role import Role, RoleNames, user_roles,  create_roles
from .annotation import Annotation
from .project import Project
from .task import Task


def create_db_defaults(app: Flask) -> None:
    with app.app_context():
        create_roles()
        create_default_super_admin()
