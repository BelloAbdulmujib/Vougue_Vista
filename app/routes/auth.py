from flask import Flask, Blueprint, request, jsonify, render_template, url_for, redirect, flash
from app import db
from flask_login import login_user, logout_user
from app.form import LoginForm, SignupForm
from app.models import User, Admin
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    print("in the login route")
    """Handles the login for both users and admins."""
    form = LoginForm()
    #if form.validate_on_submit():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the email exists in the User or Admin table
        user = User.query.filter_by(email=email).first()
        
        # uncomment later
        # admin = Admin.query.filter_by(email=email).first()

        # If the user exists and the password is correct
        if user and check_password_hash(user.password, password):
            login_user(user)
            print('user logged in successfuly')
            flash('User logged in successfully!', 'success')
            return redirect(url_for('home'))  #

        # If the admin exists and the password is correct
        # elif admin and admin.check_password(password):
        #     login_user(admin)
        #     flash('Admin logged in successfully!', 'success')
        #     return redirect(url_for('admin'))  # Redirect to admin dashboard
        
        # # If the credentials are incorrect
        # else:
        #     flash('Invalid email or password', 'danger')
        #     return redirect(url_for('auth.login'))

    # Render the login page if it's a GET request or after an invalid POST request
    return render_template('auth/login.html', title='Login', form=form)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handles the signup form for a new user"""
    form = SignupForm()
    
    if form.validate_on_submit():
        # Extract form data correctly using form object
        email = form.email.data
        password = form.password.data
        username = form.username.data

        # Checks if the user already exists
        if User.query.filter_by(email=email).first():
            flash("User with this email already exists", "error")
            return redirect(url_for('auth.signup')), 400

        # Hash the password (This ensures hash_password is working as expected)
        hashed_password = generate_password_hash(password)
        
        # Create a new user object and save it to the database
        user = User(username=username, email=email, password=hashed_password)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash('An error occurred while creating the account. Please try again.', 'danger')
            print(f"Error creating user: {e}")  # Log the error for debugging
            return redirect(url_for('auth.signup')), 500
    
    # If there are form validation errors
    if form.errors:
        print("Form validation errors:", form.errors)
        flash('Please correct the errors in the form.', 'danger')

    # Render the signup page with the form
    return render_template('auth/signup.html', title='Signup', form=form)


@auth_bp.route('/logout')
def logout():
    """ Handles the logout """
    logout_user()
    return redirect(url_for('auth.login'))