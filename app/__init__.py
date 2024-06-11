# Import necessary modules from Flask and other libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from dotenv import load_dotenv
from config import config
from flask_wtf.csrf import CSRFProtect

# Load environment variables from a .env file
load_dotenv()

# Initialize CSRF protection
csrf = CSRFProtect()

# Initialize the database, migration tool, and login manager
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name):
    """
    Creates and configures an instance of the Flask application.

    Args:
        config_name (str): The configuration name to use for the application.
    
    Returns:
        Flask: The configured Flask application instance.
    """
    # Create the Flask application instance
    app = Flask(__name__, instance_relative_config=True)
    
    # Set the secret key for session management and CSRF protection
    app.config['SECRET_KEY'] = 'secret-key'
    
    # Set the database URI for SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_tracker.db'
    
    # Load the configuration from the config object
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize the extensions with the application instance
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    CORS(app)

    # Import and register blueprints for authentication and main functionality
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints with URL prefixes
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)

    return app

# Import models to ensure they are registered with SQLAlchemy
from . import models

@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user by their user ID.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        User: The User object if found, otherwise None.
    """
    return models.User.query.get(int(user_id))
