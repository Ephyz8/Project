from flask.cli import FlaskGroup
from app import create_app, db

def create_my_app():
    return create_app('development')  # Or 'production', 'testing', etc.

cli = FlaskGroup(create_app=create_my_app)

@cli.command("create_db")
def create_db():
    with create_my_app().app_context():
        db.create_all()
        db.session.commit()

@cli.command("drop_db")
def drop_db():
    with create_my_app().app_context():
        db.drop_all()
        db.session.commit()

if __name__ == "__main__":
    cli()
