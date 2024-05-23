from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .models import User, Activity, HealthMetric
from .forms import RegistrationForm, LoginForm
from . import db

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    """
    A user loader callback used to reload the user object from the user ID stored in the session.
    """
    return User.query.get(int(user_id))

@main.route('/')
def home():
    """
    Handles the root URL ('/') and renders the home page template (index.html).
    """
    return render_template('index.html')

@main.route('/about')
def about():
    """
    Handles the URL path '/about' and renders the about page template (about.html).
    """
    return render_template('about.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Handles the URL path '/contact' and supports both GET and POST methods.
    """
    if request.method == 'POST':
        # Handle form submission (e.g., send an email or save to a database)
        return redirect(url_for('main.home'))
    return render_template('contact.html')

@main.route('/metrics', methods=['GET'])
@login_required
def get_metrics():
    metrics = HealthMetric.query.filter_by(user_id=current_user.id).all()
    metrics_data = [{"metric_type": m.metric_type, "value": m.value, "date": m.date.strftime('%Y-%m-%d')} for m in metrics]
    return jsonify(metrics_data), 200

@main.route('/metrics_data')
@login_required
def metrics_data():
    metrics = HealthMetric.query.filter_by(user_id=current_user.id).all()
    metrics_data = {
        'labels': [m.date.strftime('%Y-%m-%d') for m in metrics],
        'values': [m.value for m in metrics]
    }
    return jsonify(metrics_data)

@main.route('/metrics', methods=['POST'])
@login_required
def create_metric():
    data = request.get_json()
    new_metric = HealthMetric(
        user_id=current_user.id,
        metric_type=data['metric_type'],
        value=data['value'],
        date=datetime.strptime(data['date'], '%Y-%m-%d') if 'date' in data else datetime.utcnow()
    )
    db.session.add(new_metric)
    db.session.commit()
    return jsonify({'message': 'Metric added successfully'}), 201

@main.route('/metrics/<int:metric_id>', methods=['PUT'])
@login_required
def update_metric(metric_id):
    data = request.get_json()
    metric = HealthMetric.query.get_or_404(metric_id)
    if metric.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    metric.metric_type = data.get('metric_type', metric.metric_type)
    metric.value = data.get('value', metric.value)
    metric.date = datetime.strptime(data['date'], '%Y-%m-%d') if 'date' in data else metric.date

    db.session.commit()
    return jsonify({'message': 'Metric updated successfully'}), 200

@main.route('/metrics/<int:metric_id>', methods=['DELETE'])
@login_required
def delete_metric(metric_id):
    metric = HealthMetric.query.get_or_404(metric_id)
    if metric.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403

    db.session.delete(metric)
    db.session.commit()
    return jsonify({'message': 'Metric deleted successfully'}), 200

@main.route('/users', methods=['POST'])
def create_user():
    """Handles the creation of a new user."""
    data = request.get_json()
    existing_user = User.query.filter_by(username=data['username']).first()
    existing_email = User.query.filter_by(email=data['email']).first()
    if existing_user or existing_email:
        return jsonify({'error': 'Username or email already exists!'}), 400

    new_user = User(
        username=data['username'], 
        email=data['email'], 
        password=generate_password_hash(data['password'], method='sha256')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created!'}), 201

@main.route('/log_activity', methods=['GET', 'POST'])
@login_required
def log_activity():
    """
    Handles the logging of a new activity.
    """
    if request.method == 'POST':
        activity_type = request.form['activity_type']
        duration = request.form['duration']
        new_activity = Activity(
            activity_type=activity_type, 
            duration=int(duration), 
            user_id=current_user.id,
            timestamp=datetime.utcnow()
        )
        db.session.add(new_activity)
        db.session.commit()
        return redirect(url_for('main.activities'))
    return render_template('log_activity.html', title='Log Activity')

@main.route('/activities')
@login_required
def activities():
    """
    Handles retrieving all logged activities for the current user.
    """
    user_activities = Activity.query.filter_by(user_id=current_user.id).all()
    return render_template('activities.html', activities=user_activities)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if existing_user or existing_email:
            flash('Username or email already exists!', 'error')
            return redirect(url_for('auth.register'))
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.
    """
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        flash('Login failed. Check your email and password.', 'error')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """
    Handles user logout.
    """
    logout_user()
    return redirect(url_for('auth.login'))

# User profile management routes
@main.route('/profile', methods=['GET'])
@login_required
def get_profile():
    user = User.query.get_or_404(current_user.id)
    profile_data = {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "bio": user.bio,
        "location": user.location,
        "date_of_birth": user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else None
    }
    return jsonify(profile_data), 200

@main.route('/profile', methods=['POST'])
@login_required
def create_or_update_profile():
    data = request.get_json()
    # Basic validation
    if 'date_of_birth' in data:
        try:
            datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    user = User.query.get_or_404(current_user.id)
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.bio = data.get('bio', user.bio)
    user.location = data.get('location', user.location)
    user.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d') if 'date_of_birth' in data else user.date_of_birth

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200

@main.route('/profile', methods=['DELETE'])
@login_required
def delete_profile():
    user = User.query.get_or_404(current_user.id)
    db.session.delete(user)
    db.session.commit()
    logout_user()
    return jsonify({'message': 'Profile deleted successfully'}), 200

# Main routes
@main.route('/dashboard')
@login_required
def dashboard():
    """
    Renders the user dashboard.
    """
    return render_template('dashboard.html', name=current_user.username)
