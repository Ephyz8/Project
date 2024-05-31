from app import db
db.engine.execute("PRAGMA table_info(mood)").fetchall()
