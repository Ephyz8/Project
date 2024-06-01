from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, FloatField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Optional
from datetime import datetime

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional(), Length(max=100)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=100)])
    bio = TextAreaField('Bio', validators=[Optional()])
    location = StringField('Location', validators=[Optional(), Length(max=100)])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Update Profile')

class DeleteProfileForm(FlaskForm):
    submit = SubmitField('Delete Profile')
    
class ActivityForm(FlaskForm):
    steps = IntegerField('Steps', validators=[DataRequired()])
    distance = FloatField('Distance (in km)', validators=[DataRequired()])
    calories = IntegerField('Calories', validators=[DataRequired()])
    type = SelectField('Activity Type', choices=[
        ('Walking', 'Walking'),
        ('Running', 'Running'),
        ('Cycling', 'Cycling'),
        ('Swimming', 'Swimming'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    duration = IntegerField('Duration (in minutes)', validators=[DataRequired()])
    submit = SubmitField('Log Activity')

class NutritionForm(FlaskForm):
    calories = IntegerField('Calories', validators=[DataRequired(), NumberRange(min=0)])
    protein = FloatField('Protein (grams)', validators=[DataRequired(), NumberRange(min=0)])
    carbs = FloatField('Carbs (grams)', validators=[DataRequired(), NumberRange(min=0)])
    fats = FloatField('Fats (grams)', validators=[DataRequired(), NumberRange(min=0)])
    date = DateField('Date', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Log Nutrition')

class SleepForm(FlaskForm):
    hours = FloatField('Hours Slept', validators=[DataRequired(), NumberRange(min=0)])
    quality = SelectField('Quality', choices=[('Poor', 'Poor'), ('Fair', 'Fair'), ('Good', 'Good'), ('Excellent', 'Excellent')], validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Log Sleep')

class MoodForm(FlaskForm):
    mood = SelectField('Mood', choices=[('Very Bad', 'Very Bad'), ('Bad', 'Bad'), ('Neutral', 'Neutral'), ('Good', 'Good'), ('Very Good', 'Very Good')], validators=[DataRequired()])
    notes = TextAreaField('Note', validators=[Optional()])
    date = DateField('Date', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Log Mood')
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=10)])
    
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')

