from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from .models import User, Activity
from werkzeug.security import generate_password_hash, check_password_hash
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

@main.route('/users', methods=['POST'])
def create_user():
    """Handles the creation of a new user."""
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'], password=generate_password_hash(data['password'], method='sha256'))
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
        activity_name = request.form['activity_name']
        duration = request.form['duration']
        new_activity = Activity(name=activity_name, duration=duration, user_id=current_user.id)
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

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Main routes
@main.route('/dashboard')
@login_required
def dashboard():
    """
    Renders the user dashboard.
    """
    return render_template('dashboard.html', name=current_user.username)
