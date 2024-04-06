from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "db.sqlite"

# create an app
def create_app():
    app = Flask(__name__)
    
    app.config["SECRET_KEY"] = 'noor_2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    
    from . import models 
    with app.app_context():
        db.create_all()
    
    # Set the Login Manager to remember user is loged in
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .models import Users
    @login_manager.user_loader
    def user_loader(user_id):
        return Users.query.get(int(user_id))
    # register main bluepring
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # register authontication bluepring
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    # return the app
    return app
