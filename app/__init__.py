from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config_by_name

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    """Creates and configures an instance of the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_tracker.db'
    app.config['SQLACHEMY_TRACK_MODIFCATIONS'] = False
    app.config['SECRET_KEY'] = 'cebcacf23f96a1640f40153a4790fe32'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    migrate.init_app()
    login_manager.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app
