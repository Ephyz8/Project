from sqlalchemy import create_engine, MetaData
from yourapp import app, db

# Ensure you have the correct path to your SQLite database
DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']

def drop_all_tables():
    engine = create_engine(DATABASE_URI)
    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(bind=engine)
    print("All tables dropped.")

if __name__ == "__main__":
    drop_all_tables()
