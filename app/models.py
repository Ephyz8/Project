from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """
    Defines a User class that inherits from db.Model, making it a model class for SQLAlchemy.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    activities = db.relationship('Activity', backref='user', lazy=True)
    nutrition_entries = db.relationship('Nutrition', backref='user', lazy=True)
    sleep_entries = db.relationship('Sleep', backref='user', lazy=True)
    mood_entries = db.relationship('Mood', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'bio': self.bio,
            'location': self.location,
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d') if self.date_of_birth else None,
        }

class Activity(db.Model):
    """
    Defines an Activity class that inherits from db.Model, making it a model class for SQLAlchemy.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    steps = db.Column(db.Integer, nullable=True)
    distance = db.Column(db.Float, nullable=True)  # Distance in kilometers
    calories_burned = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Activity {self.activity_type}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'duration': self.duration,
            'steps': self.steps,
            'distance': self.distance,
            'calories_burned': self.calories_burned,
            'timestamp': self.timestamp
        }

class Nutrition(db.Model):
    """
    Defines a Nutrition class that inherits from db.Model, making it a model class for SQLAlchemy.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Nutrition {self.date}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date,
            'calories': self.calories,
            'protein': self.protein,
            'fat': self.fat,
            'carbs': self.carbs
        }

class Sleep(db.Model):
    """
    Defines a Sleep class that inherits from db.Model, making it a model class for SQLAlchemy.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    hours = db.Column(db.Float, nullable=False)
    quality = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Sleep {self.date}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date,
            'hours': self.hours,
            'quality': self.quality
        }

class Mood(db.Model):
    """
    Defines a Mood class that inherits from db.Model, making it a model class for SQLAlchemy.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    rating = db.Column(db.Integer, nullable=False)  # Scale of 1-10
    notes = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Mood {self.date}>'

    def to_dict(self):
        return {
            'mood': self.mood,
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date,
            'rating': self.rating,
            'notes': self.notes
        }
