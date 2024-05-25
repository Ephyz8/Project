from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    """Creates and configures an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from .routes import main, 
    from . import auth

    login_manager.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    return app

from . import models

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))
