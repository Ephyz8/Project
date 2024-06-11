from flask.cli import FlaskGroup
from app import create_app, db

def create_my_app():
    """
    Factory function that creates and configures the Flask application.
    """
    return create_app('development')  # Change to 'production', 'testing', etc., as needed

# Create an instance of FlaskGroup, passing the application factory function
cli = FlaskGroup(create_app=create_my_app)

@cli.command("create_db")
def create_db():
    """
    CLI command to create the database tables.
    """
    with create_my_app().app_context():
        db.create_all()  # Create all tables defined by the models
        db.session.commit()  # Commit the changes to the database
        print("Database tables created successfully.")

@cli.command("drop_db")
def drop_db():
    """
    CLI command to drop the database tables.
    """
    with create_my_app().app_context():
        db.drop_all()  # Drop all tables defined by the models
        db.session.commit()  # Commit the changes to the database
        print("Database tables dropped successfully.")

if __name__ == "__main__":
    cli()  # Run the Flask CLI
