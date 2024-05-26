from app import create_app, db
from app.models import User, Activity, HealthMetric
from werkzeug.security import generate_password_hash
from datetime import datetime

def seed():
    app = create_app('production')

    with app.app_context():
        db.drop_all()
        db.create_all()

    # Create sample user
    user1 = User(
        username='testuser',
        email='test@example.com',
        password=generate_password_hash('password', method='pbkdf2:sha256')
    )

    db.session.add(user1)
    db.session.commit()

    # Create sample activities
    activity1 = Activity(
        user_id=user1.id,
        activity_type='Running',
        duration=30,
        timestamp=datetime.utcnow()
    )
    activity2 = Activity(
        user_id=user1.id,
        activity_type='Swimming',
        duration=45,
        timestamp=datetime.utcnow()
    )

    db.session.add(activity1)
    db.session.add(activity2)
    db.session.commit()

    # Create sample health metrics
    metric1 = HealthMetric(
        user_id=user1.id,
        metric_type='weight',
        value=70.5,
        date=datetime.utcnow()
    )
    metric2 = HealthMetric(
        user_id=user1.id,
        metric_type='blood_pressure',
        value=120,
        date=datetime.utcnow()
    )

    db.session.add(metric1)
    db.session.add(metric2)
    db.session.commit()

    print('Database seeded successfully!')

if __name__ == '__main__':
    seed()
