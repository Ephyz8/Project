from app import create_app
from config import config_by_name

app = create_app(config_name)

if __name__ == "__main__":
    app.run()
