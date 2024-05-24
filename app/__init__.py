from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config_by_name
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_name):
    """Creates and configures an instance of the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_tracker.db'
    app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False
    app.config['SECRET_KEY'] = 'cebcacf23f96a1640f40153a4790fe32'

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from .routes import main, auth
    # from app.api import api as api_blueprint

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    # app.register_blueprint(api_blueprint, url_prefix='/api')

    return app

from . import models

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))
