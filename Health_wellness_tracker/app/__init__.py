from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """Creates and configures an instance of the Flask application.
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_tracker.db'
    app.config['SQLACHEMY_TRACK_MODIFCATIONS'] = False

    db.init_app(app)
    migrate.init_app()

    from .routes import main
    app.register_blueprint(main)

    return app
