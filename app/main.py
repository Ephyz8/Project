from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user
from datetime import datetime
from .models import User, Activity, Nutrition, Sleep, Mood
from . import db
from .forms import ProfileForm

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thank you for contacting us!', 'success')
        return redirect(url_for('main.home'))
    return render_template('contact.html')

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
    return render_template('dashboard.html', name=current_user.username)

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
