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
    metrics = db.relationship('HealthMetric', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        """
        Special method that returns a string representation of the object.
        It's useful for debugging and logging.
        """
        return f'<User {self.username}>'
    
    def to_dict(self):
        """
        Converts the user instance into a dictionary.
        It's useful for serializing the object to JSON when returning responses from the API.
        """
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
    Defines an Activity class that inherits from db.Model,
    making it a model class for SQLAlchemy.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        """
        Special method that returns a string representation of the object.
        It's useful for debugging and logging.
        """
        return f'<Activity {self.activity_type}>'

    def to_dict(self):
        """
        Converts the activity instance into a dictionary.
        It's useful for serializing the object to JSON when returning responses from the API.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'duration': self.duration,
            'timestamp': self.timestamp
        }

class HealthMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    metric_type = db.Column(db.String(50), nullable=False)  # e.g., weight, blood_pressure
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
 
    def __repr__(self):
        """
        Special method that returns a string representation of the object.
        It's useful for debugging and logging.
        """
        return f'<HealthMetric {self.metric_type}>'
    
    def to_dict(self):
        """
        Converts the activity instance into a dictionary.
        It's useful for serializing the object to JSON when returning responses from the API.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'metric_type': self.metric_type,
            'value': self.value,
            'date': self.date
        }
