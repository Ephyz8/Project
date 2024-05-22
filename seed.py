from app import create_app, db
from app.models import User, Activity, HealthMetric
from werkzeug.security import generate_password_hash

app = create_app('dev')

def create_initial_data():
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(
            username='testuser',
            email='test@example.com',
            password=generate_password_hash('password', method='sha256')
        )
        db.session.add(user)
        db.session.commit()
        print('Database has been initialized and seeded.')

if __name__ == '__main__':
    create_initial_data()
