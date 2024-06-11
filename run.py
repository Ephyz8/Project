import os
from app import create_app

# Create the Flask application using the 'development' configuration
app = create_app('development')

if __name__ == "__main__":
    # Run the Flask development server on the specified host and port
    # Default port is 10000, but can be overridden by the PORT environment variable
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
