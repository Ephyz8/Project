import os
from config import config
from app import create_app

# Determine the configuration to use based on the FLASK_ENV environment variable
# Defaults to 'default' if FLASK_ENV is not set
config_name = os.getenv('FLASK_ENV', 'default')

# Create the Flask application using the specified configuration
app = create_app(config_name)

if __name__ == "__main__":
    # Run the Flask application with debugging enabled
    # This line is typically only executed in a development environment
    app.run(debug=True)