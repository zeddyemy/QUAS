from flask_admin import Admin
from flask_admin.menu import MenuLink

from ....models import AppUser, Media
from ....extensions import db
from .admin_views import AppAdminIndexView, UserView


flask_app_admin = Admin(name="Cpanel", index_view=AppAdminIndexView(template="cpanel/index.html", url="/cpanel"), template_mode="bootstrap3")

def setup_flask_admin(app):
    flask_app_admin.init_app(app)
    
    # Add custom links
    flask_app_admin.add_link(MenuLink(name='Logout', category='', url='/cpanel/logout'))
    
    # Add views with restricted access
    flask_app_admin.add_view(UserView(AppUser, db.session, "Users"))