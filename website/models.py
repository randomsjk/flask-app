from . import db, login_manager
from sqlalchemy.sql import func
from flask_login import UserMixin

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(300))
    complete = db.Column(db.Boolean, default = False)
    date_created = db.Column(db.String(300), default = func.now())
    userid = db.Column(db.Integer)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)