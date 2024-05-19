from flask import Blueprint, render_template, request, jsonify
from .models import db, User, Activity

main = Blueprint('main', __name__)


@main.route('/')
def home():
    """
    Handles the root URL ('/') and renders the home page template (index.html). 
    Returns:
        Response: An HTML page generated from the 'index.html' template.
    """
    return render_template('index.html')

@main.route('/about')
def about():
    """
    Handles the URL path '/about' and renders the about page template (about.html).
    Returns:
    Response: An HTML page generated from the 'about.html' template.
    """
    return render_template('about.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Handles the URL path '/contact' and supports both GET and POST methods.
    - For GET requests, it renders the contact page template (contact.html).
    - For POST requests, it processes the submitted form data and redirects to the home page.

    POST Handling:
    - Processes the form submission.
    - Redirects the user to the home page after processing.

    Returns:
    Response: 
    - For GET requests, an HTML page generated from the 'contact.html' template.
    - For POST requests, a redirection to the home page.
    """
    if request.method == 'POST':
      # Handle form submission (e.g., send an email or save to a database)
      return redirect(url_for('main.home'))
    return render_template('contact.html')

@main.route('/users', methods=['POST'])
def create_user():
    """Handles the creation of a new user."""

    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created!'}), 201

@main.route('/activities', methods=['GET'])
def get_activities():
    """Handles retrieving all logged activities."""
    
    activities = Activity.query.all()
    return jsonify([activity.to_dict() for activity in activities]), 200







