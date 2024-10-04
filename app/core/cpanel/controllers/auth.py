# from werkzeug.urls import url_parse
from urllib.parse import urlparse
from flask import render_template, request, Response, flash, redirect, url_for, abort
from flask_login import login_user, logout_user, current_user

from ....utils.helpers.loggers import console_log
from ....utils.helpers.users import get_app_user
from ....utils.helpers.basics import redirect_url
from ....utils.forms.auth import LoginForm


class CPanelAuthController:
    @staticmethod
    def login():
        form: LoginForm = LoginForm()
    
        if current_user.is_authenticated:
            return redirect(redirect_url("admin.index"))
        
        if request.method == "POST":
            if form.validate_on_submit():
                console_log("form", request.form)
                
                email_username = form.email_username.data
                pwd = form.pwd.data
                
                
                # get next argument fro url
                next = request.args.get("next")
                if not next or urlparse(next).netloc != "":
                    next = url_for("admin.index")
                
                
                # get user from db with the email/username.
                user = get_app_user(email_username)
                
                if user:
                    if user.check_password(pwd):
                        login_user(user)
                        flash("Welcome back " + user.username, "success")
                        return redirect(next)
                    else:
                        flash("Incorrect password", "error")
                else:
                    flash("Email or Username is incorrect or doesn't exist", "error")
                
            else:
                console_log("Form Errors", form.errors)
                flash("Something went Wrong. Please Try Again.", "error")
        
        return render_template("cpanel/auth/login.html", form=form, page="auth")
    
    @staticmethod
    def logout():
        logout_user()
        return redirect(url_for("cpanel.login"))