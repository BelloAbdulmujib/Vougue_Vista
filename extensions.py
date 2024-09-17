from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login = LoginManager()

@login.user_loader
def user_loader(user_id):
    """ This function loads the user from the database """
    from app.models import User
    return User.query.get(int(user_id))