import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get the base directory of the application
basedir = os.path.abspath(os.path.dirname(__file__))
# Define the instance directory path
instance_dir = os.path.join(basedir, 'instance')

class Config:
    """Base configuration class."""
    # Secret key for session management and other security-related tasks
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    # Disable tracking modifications of objects and emit signals
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # URI for the SQLite database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(instance_dir, 'health_tracker.db')
    # Headers for Cross-Origin Resource Sharing (CORS)
    CORS_HEADERS = 'Content-Type'
    # Enable Cross-Site Request Forgery (CSRF) protection
    WTF_CSRF_ENABLED = True

    @staticmethod
    def init_app(app):
        # Static method to initialize the app with additional settings if needed
        pass

class DevelopmentConfig(Config):
    """Development configuration."""
    # Enable debugging mode in development
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    # Enable testing mode
    TESTING = True
    # URI for the test SQLite database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(instance_dir, 'test_health_tracker.db')
    # Disable CSRF protection in testing
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration."""
    # Disable debugging mode in production
    DEBUG = False

# Dictionary to map configuration names to configuration classes
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
