from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from .models import User, Activity, Nutrition, Sleep, Mood
from . import db
from .forms import DeleteProfileForm, ProfileForm, SleepForm, ContactForm, MoodForm, ActivityForm, NutritionForm
import json

main = Blueprint('main', __name__)

@main.route('/')
def home():
    """
    Route for the home page.
    """
    return render_template('index.html')

@main.route('/about')
def about():
    """
    Route for the about page.
    """
    return render_template('about.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Route for the contact page. Handles contact form submissions.
    """
    form = ContactForm()
    if form.validate_on_submit():
        # Process the form data
        flash('Thank you for contacting us!', 'success')
        return redirect(url_for('main.home'))
    return render_template('contact.html', form=form)

@main.route('/users', methods=['POST'])
def create_user():
    """
    API route to create a new user. Expects JSON data.
    """
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

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def create_or_update_profile():
    """
    Route to create or update the user's profile.
    """
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        current_user.date_of_birth = form.date_of_birth.data
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('main.dashboard'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.bio.data = current_user.bio
        form.location.data = current_user.location
        form.date_of_birth.data = current_user.date_of_birth
    return render_template('profile.html', title='Profile', form=form)

@main.route('/delete_profile', methods=['POST'])
@login_required
def delete_profile():
    """
    Route to delete the user's profile and all associated data.
    """
    form = DeleteProfileForm()
    if form.validate_on_submit():
        user_id = current_user.id

        # Delete all associated records
        Activity.query.filter_by(user_id=user_id).delete()
        Nutrition.query.filter_by(user_id=user_id).delete()
        Sleep.query.filter_by(user_id=user_id).delete()
        Mood.query.filter_by(user_id=user_id).delete()
        
        # Now delete the user
        user = User.query.filter_by(id=user_id).first_or_404()
        logout_user()  # Log out the user before deleting the profile
        db.session.delete(user)
        db.session.commit()

        flash('Your profile has been deleted.', 'success')
        return redirect(url_for('main.home'))
    return render_template('profile.html', title='Profile', delete_form=form)

@main.route('/dashboard_data')
@login_required
def dashboard():
    """
    Route to display the dashboard data for the current user.
    """
    user_id = current_user.id

    sleep_data = Sleep.query.filter_by(user_id=user_id).all()
    total_sleep_hours = sum(s.hours for s in sleep_data)
    avg_sleep_hours = total_sleep_hours / len(sleep_data) if sleep_data else 0

    nutrition_data = Nutrition.query.filter_by(user_id=user_id).all()
    total_calories = sum(n.calories for n in nutrition_data)

    mood_data = Mood.query.filter_by(user_id=user_id).all()
    mood_counts = {}
    for mood in mood_data:
        mood_counts[mood.rating] = mood_counts.get(mood.rating, 0) + 1

    return render_template(
        'dashboard.html', 
        name=current_user.username, 
        avg_sleep_hours=avg_sleep_hours, 
        total_calories=total_calories, 
        mood_counts=json.dumps(mood_counts)
    )

@main.route('/log_sleep', methods=['GET', 'POST'])
@login_required
def log_sleep():
    """
    Route to log sleep data for the current user.
    """
    form = SleepForm()
    if form.validate_on_submit():
        sleep = Sleep(
            user_id=current_user.id,
            hours=form.hours.data,
            quality=form.quality.data,
            date=datetime.utcnow().date()
        )
        db.session.add(sleep)
        db.session.commit()
        flash('Sleep logged successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('log_sleep.html', title='Log Sleep', form=form)

@main.route('/sleep_data', methods=['GET'])
@login_required
def sleep_data():
    """
    API route to get sleep data for the current user based on the period.
    """
    period = request.args.get('period', 'daily')
    sleeps = get_sleeps_by_period(current_user.id, period)
    sleep_data = [{
        "hours": sleep.hours,
        "quality": sleep.quality,
        "date": sleep.date.strftime('%Y-%m-%d')
    } for sleep in sleeps]
    return jsonify(sleep_data), 200

@main.route('/log_mood', methods=['GET', 'POST'])
@login_required
def log_mood():
    """
    Route to log mood data for the current user.
    """
    form = MoodForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_mood = Mood(
            user_id=current_user.id,
            rating=form.rating.data,
            notes=form.notes.data,
            date=datetime.utcnow().date()
        )
        db.session.add(new_mood)
        db.session.commit()
        flash('Mood logged successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('log_mood.html', form=form)

@main.route('/mood_data', methods=['GET'])
@login_required
def mood_data():
    """
    API route to get mood data for the current user based on the period.
    """
    period = request.args.get('period', 'daily')
    moods = get_moods_by_period(current_user.id, period)
    mood_data = [{
        "rating": mood.rating,
        "notes": mood.notes,
        "date": mood.date.strftime('%Y-%m-%d')
    } for mood in moods]
    return jsonify(mood_data), 200

@main.route('/log_activity', methods=['GET', 'POST'])
@login_required
def log_activity():
    """
    Route to log physical activity data for the current user.
    """
    form = ActivityForm()
    if form.validate_on_submit():
        activity = Activity(
            user_id=current_user.id,
            steps=form.steps.data,
            distance=form.distance.data,
            calories=form.calories.data,
            type=form.type.data,
            duration=form.duration.data,
            date=datetime.utcnow()
        )
        db.session.add(activity)
        db.session.commit()
        flash('Activity logged successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('log_activity.html', form=form)

@main.route('/activity_data', methods=['GET'])
@login_required
def activity_data():
    """
    API route to get activity data for the current user based on the period.
    """
    period = request.args.get('period', 'daily')
    activities = get_activities_by_period(current_user.id, period)
    activity_data = [{
        "steps": a.steps,
        "distance": a.distance,
        "calories": a.calories,
        "type": a.type,
        "duration": a.duration,
        "date": a.date.strftime('%Y-%m-%d')
    } for a in activities]
    return jsonify(activity_data), 200

@main.route('/log_nutrition', methods=['GET', 'POST'])
@login_required
def log_nutrition():
    """
    Route to log nutrition data for the current user.
    """
    form = NutritionForm()
    if form.validate_on_submit():
        nutrition = Nutrition(
            user_id=current_user.id,
            calories=form.calories.data,
            protein=form.protein.data,
            carbs=form.carbs.data,
            fats=form.fats.data,
            date=datetime.utcnow().date()
        )
        db.session.add(nutrition)
        db.session.commit()
        flash('Nutrition logged successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('log_nutrition.html', title='Log Nutrition', form=form)

@main.route('/nutrition_data', methods=['GET'])
@login_required
def nutrition_data():
    """
    API route to get nutrition data for the current user based on the period.
    """
    period = request.args.get('period', 'daily')
    nutritions = get_nutritions_by_period(current_user.id, period)
    nutrition_data = [{
        "calories": n.calories,
        "protein": n.protein,
        "carbs": n.carbs,
        "fats": n.fats,
        "date": n.date.strftime('%Y-%m-%d')
    } for n in nutritions]
    return jsonify(nutrition_data), 200

def get_activities_by_period(user_id, period):
    """
    Helper function to get activities based on the specified period.
    """
    now = datetime.utcnow()
    if period == 'daily':
        start_date = now - timedelta(days=1)
    elif period == 'weekly':
        start_date = now - timedelta(weeks=1)
    elif period == 'monthly':
        start_date = now - timedelta(days=30)
    else:
        start_date = now - timedelta(days=1)
    return Activity.query.filter(Activity.user_id == user_id, Activity.date >= start_date).all()

def get_nutritions_by_period(user_id, period):
    """
    Helper function to get nutrition data based on the specified period.
    """
    now = datetime.utcnow()
    if period == 'daily':
        start_date = now - timedelta(days=1)
    elif period == 'weekly':
        start_date = now - timedelta(weeks=1)
    elif period == 'monthly':
        start_date = now - timedelta(days=30)
    else:
        start_date = now - timedelta(days=1)
    return Nutrition.query.filter(Nutrition.user_id == user_id, Nutrition.date >= start_date).all()

def get_sleeps_by_period(user_id, period):
    """
    Helper function to get sleep data based on the specified period.
    """
    now = datetime.utcnow()
    if period == 'daily':
        start_date = now - timedelta(days=1)
    elif period == 'weekly':
        start_date = now - timedelta(weeks=1)
    elif period == 'monthly':
        start_date = now - timedelta(days=30)
    else:
        start_date = now - timedelta(days=1)
    return Sleep.query.filter(Sleep.user_id == user_id, Sleep.date >= start_date).all()

def get_moods_by_period(user_id, period):
    """
    Helper function to get mood data based on the specified period.
    """
    now = datetime.utcnow()
    if period == 'daily':
        start_date = now - timedelta(days=1)
    elif period == 'weekly':
        start_date = now - timedelta(weeks=1)
    elif period == 'monthly':
        start_date = now - timedelta(days=30)
    else:
        start_date = now - timedelta(days=1)
    return Mood.query.filter(Mood.user_id == user_id, Mood.date >= start_date).all()
