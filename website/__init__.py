from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()  # This is the object we use whenever we want to add something to the database (create new user e.g.)
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)  # represents the name of the file that was rum
    app.config['SECRET_KEY'] = 'This is my first website and it will be awesome!'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # sqlite/ sqlalchemy database is located at this location
    db.init_app(app)
    # initialize database by giving flask app
    # <- takes this database that we defined here and tells this is the app we are going to use

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
