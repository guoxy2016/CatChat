from flask_login import LoginManager, AnonymousUserMixin
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
moment = Moment()

login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))


class Guest(AnonymousUserMixin):
    @property
    def is_admin(self):
        return False


login_manager.anonymous_user = Guest
