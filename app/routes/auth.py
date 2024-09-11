from flask import Flask, Blueprint, request, jsonify, render_template, url_for, redirect, flash
import re
from app import db
from flask_login import login_user, logout_user
from app.form import LoginForm, SignupForm
from app.models import User, Admin
import uuid

auth_bp = Blueprint('auth', __name__)

def strong_password(password):
    # Regular expression to confirm strong password
    import re
    if (len(password) >= 8 and
        re.search(r'[a-z]', password) and
        re.search(r'[A-Z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[@$!%*?&]', password)):
        return True
    return False
    """pattern = re.compile(r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
    return pattern.match(password) is not None"""


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """handles the user and admin login"""
    form = LoginForm()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        admin = Admin.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return jsonify({"message": "User logged in successfully!"})
        elif admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))  # Redirect to the admin dashboard
        else:
            flash("Invalid email or password", 'danger')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html', title='Login', user='user')  # Render the login form if it's a GET request



@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Handles the signup form for a new user"""
    form = SignupForm()
    if form.validate_on_submit():
        # This will extract form data
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash("User already exists", "error")
            return redirect(url_for('auth.signup')), 400

        if not email or not password:
            return jsonify({"message": "Email and password required"})

        """if User.query.filter_by(email=form.email.data).first():
            return jsonify({"message": "User already exist"}), 400"""

        if not strong_password(password):
            flash("Password does not meet the requirements. It must contain at least an Upper and lower case, number, and one special character, and be at least 8 characters long."), 400
            return redirect(url_for(auth.signup))

        # Proceed to create account if password meets requirement.
        # Create new user and save details to the database
        user = User(username=form.username.data, email=form.email.data, password=strong_password)

        db.session.add(user)
        db.session.commit()
        flash('Account created Successfully!'), 201
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html', title='Signup', form='form')  # Render the signup form if it's a GET request

@auth_bp.route('/logout')
def logout():
    """ Handles the logout """
    logout_user()
    return redirect(url_for('auth.login'))