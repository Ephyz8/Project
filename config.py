from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cebcacf23f96a1640f40153a4790fe32')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

# Dictionary to map the environment name to the config class
config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

class Config:
    DEBUG = False
    # Other configuration options...

class ProductionConfig(Config):
    ENV = 'production'
    # Other production configuration options...

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    # Other development configuration options...

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    # Other configuration options...
}
