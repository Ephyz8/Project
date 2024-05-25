from app import create_app, db

# Replace development with the appropriate configuration name
app = create_app('production')

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")
