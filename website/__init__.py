from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SECRET_KEY'] = 'idk lol xd'
    db.init_app(app)
    login_manager.init_app(app)

    from .views import my_view
    app.register_blueprint(my_view)

    from .models import Todo
    with app.app_context():
        db.create_all()

    return app