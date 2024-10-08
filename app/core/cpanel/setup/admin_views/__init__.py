from flask import redirect, url_for, abort, request
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from .....utils.helpers.loggers import console_log


class AppAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if not current_user or not current_user.is_authenticated:
            return False
        
        if "Super Admin" in current_user.role_names:
            return True
        
        return False

    
    def inaccessible_callback(self, name, **kwargs):
        console_log(str(current_user))
        return redirect(url_for('cpanel.login', next=request.url)) # Redirect to login page if user doesn't have access


class SuperAdminModelView(ModelView):
    def is_accessible(self):
        if not current_user or not current_user.is_authenticated:
            return False
        
        if "Super Admin" in current_user.role_names:
            return True
        
        return False

    
    def inaccessible_callback(self, name, **kwargs):
        console_log(str(current_user))
        return redirect(url_for('cpanel.login', next=request.url)) # Redirect to login page if user doesn't have access
    
    list_template = "cpanel/model/list.html"
    edit_template = "cpanel/model/edit.html"
    create_template = "cpanel/model/create.html"
    
    # can_export = True
    edit_modal = True


class UserView(SuperAdminModelView):
    can_delete = True
    form_columns = ["username", "email",  "roles"]
    column_list = ["username", "email", "roles", "date_joined"]
    
    # make columns searchable
    column_searchable_list = ['username', 'email']
    column_filters = ["username", "email"]


