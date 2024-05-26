import os
from config import config
from app import create_app

config_name = os.getenv('FLASK_ENV', 'default')
app = create_app(config_name)

if __name__ == "__main__":
    app.run() 
