# _*_ coding: utf-8 _*_
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate

bootstrap = Bootstrap()
db = SQLAlchemy()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()
csrf = CSRFProtect()
login_manager = LoginManager()
toolbar = DebugToolbarExtension()
migrate = Migrate()

@login_manager.user_loader
def load_user(user_id):
    from blueblog.models import  Admin
    user = Admin.query.get(int(user_id))
    return user

login_manager.login_view = 'auth.login'

login_manager.login_message_category = 'warning'