from . import cpanel_bp
from ..controllers import CPanelAuthController


@cpanel_bp.route("/login", methods=["GET", "POST"])
def login():
    return CPanelAuthController.login()


@cpanel_bp.route("/logout", methods=["GET", "POST"])
def logout():
    return CPanelAuthController.logout()