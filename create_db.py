from app import create_app, db

# Replace 'production' with the appropriate configuration name if needed (e.g., 'development', 'testing')
app = create_app('production')

# Use the application context to ensure the database operations are executed within the correct context
with app.app_context():
    # Create all database tables based on the models defined in the app
    db.create_all()
    print("Database tables created successfully.")
