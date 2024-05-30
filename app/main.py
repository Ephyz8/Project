from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user
from datetime import datetime, timedelta
from .models import User, Activity, Nutrition, Sleep, Mood
from . import db
from .forms import ProfileForm, ContactForm
import json

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Process the form data
        flash('Thank you for contacting us!', 'success')
        return redirect(url_for('main.home'))
    return render_template('contact.html', form=form)

@main.route('/users', methods=['POST'])
def create_user():
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

@main.route('/nutrition', methods=['POST'])
@login_required
def log_nutrition():
    data = request.get_json()
    new_nutrition = Nutrition(
        user_id=current_user.id,
        calories=data['calories'],
        protein=data['protein'],
        carbs=data['carbs'],
        fats=data['fats'],
        date=datetime.strptime(data['date'], '%Y-%m-%d') if 'date' in data else datetime.utcnow()
    )
    db.session.add(new_nutrition)
    db.session.commit()
    return jsonify({'message': 'Nutrition logged successfully'}), 201

@main.route('/sleep', methods=['POST'])
@login_required
def log_sleep():
    data = request.get_json()
    new_sleep = Sleep(
        user_id=current_user.id,
        hours=data['hours'],
        quality=data['quality'],
        date=datetime.strptime(data['date'], '%Y-%m-%d') if 'date' in data else datetime.utcnow()
    )
    db.session.add(new_sleep)
    db.session.commit()
    return jsonify({'message': 'Sleep logged successfully'}), 201

@main.route('/mood', methods=['POST'])
@login_required
def log_mood():
    data = request.get_json()
    new_mood = Mood(
        user_id=current_user.id,
        mood=data['mood'],
        note=data['note'],
        date=datetime.strptime(data['date'], '%Y-%m-%d') if 'date' in data else datetime.utcnow()
    )
    db.session.add(new_mood)
    db.session.commit()
    return jsonify({'message': 'Mood logged successfully'}), 201

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
    form = ProfileForm()
    if form.validate_on_submit():
        user = User.query.get_or_404(current_user.id)
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.bio = form.bio.data
        user.location = form.location.data
        user.date_of_birth = form.date_of_birth.data

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    flash('Form validation failed. Please correct the errors and try again.', 'error')
    return render_template('profile.html', form=form)

@main.route('/profile', methods=['DELETE'])
@login_required
def delete_profile():
    user = User.query.get_or_404(current_user.id)
    db.session.delete(user)
    db.session.commit()
    logout_user()
    flash('Profile deleted successfully.', 'success')
    return redirect(url_for('auth.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    # Fetch user's data
    user_id = current_user.id

    # Calculate average sleep hours
    sleep_data = Sleep.query.filter_by(user_id=user_id).all()
    total_sleep_hours = sum(s.hours for s in sleep_data)
    avg_sleep_hours = total_sleep_hours / len(sleep_data) if sleep_data else 0

    # Calculate total calories
    nutrition_data = Nutrition.query.filter_by(user_id=user_id).all()
    total_calories = sum(n.calories for n in nutrition_data)

    # Calculate mood trends
    mood_data = Mood.query.filter_by(user_id=user_id).all()
    mood_counts = {}
    for mood in mood_data:
        mood_counts[mood.mood] = mood_counts.get(mood.mood, 0) + 1

    return render_template(
        'dashboard.html', 
        name=current_user.username, 
        avg_sleep_hours=avg_sleep_hours, 
        total_calories=total_calories, 
        mood_counts=json.dumps(mood_counts)
    )

@main.route('/activity', methods=['POST'])
@login_required
def log_activity():
    data = request.get_json()
    new_activity = Activity(
        user_id=current_user.id,
        steps=data['steps'],
        distance=data['distance'],
        calories=data['calories'],
        type=data['type'],
        duration=data['duration']
    )
    db.session.add(new_activity)
    db.session.commit()
    return jsonify({'message': 'Activity logged successfully'}), 201

@main.route('/activity_data', methods=['POST'])
@login_required
def activity_data():
    period = request.args.get('period', 'daily')
    activities = get_activities_by_period(current_user.id, period)
    activity_data = [{
        "steps": a.steps,
        "distance": a.distance,
        "calories": a.calories,
        "type": a.type,
        "duration": a.duration,
        "timestamp": a.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for a in activities]
    return jsonify(activity_data), 200

@main.route('/nutrition_data', methods=['POST'])
@login_required
def nutrition_data():
    period = request.args.get('period', 'daily')
    nutritions = get_nutritions_by_period(current_user.id, period)
    calories = sum(n.calories for n in nutritions)
    protein = sum(n.protein for n in nutritions)
    carbs = sum(n.carbs for n in nutritions)
    fats = sum(n.fats for n in nutritions)
    return jsonify({"calories": calories, "protein": protein, "carbs": carbs, "fats": fats}), 200

@main.route('/sleep_data', methods=['POST'])
@login_required
def sleep_data():
    period = request.args.get('period', 'daily')
    sleeps = get_sleeps_by_period(current_user.id, period)
    sleep_data = [{
        "hours": s.hours,
        "quality": s.quality,
        "date": s.date.strftime('%Y-%m-%d')
    } for s in sleeps]
    return jsonify(sleep_data), 200

@main.route('/mood_data', methods=['POST'])
@login_required
def mood_data():
    period = request.args.get('period', 'daily')
    moods = get_moods_by_period(current_user.id, period)
    mood_data = [{
        "mood": m.mood,
        "note": m.note,
        "date": m.date.strftime('%Y-%m-%d')
    } for m in moods]
    return jsonify(mood_data), 200

def get_activities_by_period(user_id, period):
    now = datetime.utcnow()
    if period == 'daily':
        start_date = now - timedelta(days=1)
    elif period == 'weekly':
        start_date = now - timedelta(weeks=1)
    elif period == 'monthly':
        start_date = now - timedelta(days=30)
    else:
        start_date = now - timedelta(days=1)
    return Activity.query.filter(Activity.user_id == user_id, Activity.timestamp >= start_date).all()

def get_nutritions_by_period(user_id, period):
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
