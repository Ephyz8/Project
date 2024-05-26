import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'cebcacf23f96a1640f40153a4790fe32')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'health_tracker.db')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{DATABASE_PATH}')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///health_tracker_test.db'

class ProductionConfig(Config):
    DATABASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'health_tracker.db')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{DATABASE_PATH}')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
