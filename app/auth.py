# Import necessary modules from Flask and other libraries
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app as app
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .forms import RegistrationForm, LoginForm
from . import db

# Create a Blueprint for authentication routes
auth = Blueprint('auth', __name__, url_prefix='/auth')

# Initialize LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    """
    A user loader callback used to reload the user object from the user ID stored in the session.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        User: The User object if found, otherwise None.
    """
    return User.query.get(int(user_id))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.

    Returns:
        Response: The rendered template for the registration page or a redirect response after registration.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # Check if the username or email already exists
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if existing_user or existing_email:
            flash('Username or email already exists!', 'error')
            return redirect(url_for('auth.register'))
        
        # Hash the password and create a new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        
        # Add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error adding user: {e}")
            flash('Error: Unable to register user. Please try again.', 'error')
            return redirect(url_for('auth.register'))
    else:
        # Log validation errors for debugging
        app.logger.debug(f"Validation Errors: {form.errors}")

    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.

    Returns:
        Response: The rendered template for the login page or a redirect response after login.
    """
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        # Find the user by email
        user = User.query.filter_by(email=email).first()
        
        # Log the email and user for debugging
        app.logger.debug(f"Email entered: {email}")
        app.logger.debug(f"User found: {user}")

        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password, password):
            app.logger.debug(f"Password is correct for user: {user.username}")
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            app.logger.debug("Login failed. Either user not found or password incorrect.")
            flash('Login failed. Check your email and password.', 'error')
    else:
        # Log form validation errors for debugging
        app.logger.debug("Form validation failed.")
        app.logger.debug(form.errors)

    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """
    Handles user logout.

    Returns:
        Response: A redirect response to the login page after logout.
    """
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
