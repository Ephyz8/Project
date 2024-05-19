from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
login_manager = LoginManager()

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """Creates and configures an instance of the Flask application.
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_tracker.db'
    app.config['SQLACHEMY_TRACK_MODIFCATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    migrate.init_app()
    login_manager.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app
