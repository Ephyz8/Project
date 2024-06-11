from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, FloatField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Optional
from datetime import datetime

class RegistrationForm(FlaskForm):
    """
    Form for users to create a new account.

    Fields:
        username (StringField): Username of the user.
        email (StringField): Email address of the user.
        password (PasswordField): Password for the account.
        confirm_password (PasswordField): Confirmation of the password.
        submit (SubmitField): Submit button for the form.
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    """
    Form for users to log in to their account.

    Fields:
        email (StringField): Email address of the user.
        password (PasswordField): Password for the account.
        submit (SubmitField): Submit button for the form.
    """
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    """
    Form for users to update their profile information.

    Fields:
        first_name (StringField): First name of the user.
        last_name (StringField): Last name of the user.
        bio (TextAreaField): Short biography of the user.
        location (StringField): Location of the user.
        date_of_birth (DateField): Date of birth of the user.
        submit (SubmitField): Submit button for the form.
    """
    first_name = StringField('First Name', validators=[Optional(), Length(max=100)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=100)])
    bio = TextAreaField('Bio', validators=[Optional()])
    location = StringField('Location', validators=[Optional(), Length(max=100)])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Update Profile')

class DeleteProfileForm(FlaskForm):
    """
    Form for users to delete their profile.

    Fields:
        submit (SubmitField): Submit button for the form.
    """
    submit = SubmitField('Delete Profile')

class ActivityForm(FlaskForm):
    """
    Form for users to log their physical activities.

    Fields:
        steps (IntegerField): Number of steps taken.
        distance (FloatField): Distance covered in kilometers.
        calories (IntegerField): Calories burned.
        type (SelectField): Type of physical activity.
        duration (IntegerField): Duration of the activity in minutes.
        submit (SubmitField): Submit button for the form.
    """
    steps = IntegerField('Steps', validators=[DataRequired(), NumberRange(min=0)])
    distance = FloatField('Distance (in km)', validators=[DataRequired(), NumberRange(min=0)])
    calories = IntegerField('Calories', validators=[DataRequired(), NumberRange(min=0)])
    type = SelectField('Activity Type', choices=[
        ('Walking', 'Walking'),
        ('Running', 'Running'),
        ('Cycling', 'Cycling'),
        ('Swimming', 'Swimming'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    duration = IntegerField('Duration (in minutes)', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Log Activity')

class NutritionForm(FlaskForm):
    """
    Form for users to log their nutritional intake.

    Fields:
        calories (IntegerField): Calories consumed.
        protein (FloatField): Protein intake in grams.
        carbs (FloatField): Carbohydrate intake in grams.
        fats (FloatField): Fat intake in grams.
        date (DateField): Date of the nutritional intake.
        submit (SubmitField): Submit button for the form.
    """
    calories = IntegerField('Calories', validators=[DataRequired(), NumberRange(min=0)])
    protein = FloatField('Protein (grams)', validators=[DataRequired(), NumberRange(min=0)])
    carbs = FloatField('Carbs (grams)', validators=[DataRequired(), NumberRange(min=0)])
    fats = FloatField('Fats (grams)', validators=[DataRequired(), NumberRange(min=0)])
    date = DateField('Date', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Log Nutrition')

class SleepForm(FlaskForm):
    """
    Form for users to log their sleep details.

    Fields:
        hours (FloatField): Number of hours slept.
        quality (SelectField): Quality of sleep.
        date (DateField): Date of the sleep.
        submit (SubmitField): Submit button for the form.
    """
    hours = FloatField('Hours Slept', validators=[DataRequired(), NumberRange(min=0)])
    quality = SelectField('Quality', choices=[('Poor', 'Poor'), ('Fair', 'Fair'), ('Good', 'Good'), ('Excellent', 'Excellent')], validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Log Sleep')

class MoodForm(FlaskForm):
    """
    Form for users to log their mood.

    Fields:
        mood (SelectField): User's mood.
        notes (TextAreaField): Additional notes about the mood.
        date (DateField): Date of the mood entry.
        rating (IntegerField): Rating of the mood from 1 to 10.
        submit (SubmitField): Submit button for the form.
    """
    mood = SelectField('Mood', choices=[('Very Bad', 'Very Bad'), ('Bad', 'Bad'), ('Neutral', 'Neutral'), ('Good', 'Good'), ('Very Good', 'Very Good')], validators=[DataRequired()])
    notes = TextAreaField('Note', validators=[Optional()])
    date = DateField('Date', format='%Y-%m-%d', validators=[Optional()])
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Log Mood')

class ContactForm(FlaskForm):
    """
    Form for users to contact the support team.

    Fields:
        name (StringField): Name of the user.
        email (StringField): Email address of the user.
        message (TextAreaField): Message to the support team.
        submit (SubmitField): Submit button for the form.
    """
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')
