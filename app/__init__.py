from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from dotenv import load_dotenv
from config import config

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_name):
    """Creates and configures an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_tracker.db'
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from .routes import main, auth

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')

    return app

from . import models

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))
