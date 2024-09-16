from flask import Flask, Blueprint, request, jsonify, render_template, url_for, redirect, flash
from app import db
from flask_login import login_user, logout_user
from app.form import LoginForm, SignupForm
from app.models import User, Admin
import uuid

auth_bp = Blueprint('auth', __name__)

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
    
    return render_template('auth/login.html', title='Login', form=form)  # Render the login form if it's a GET request


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handles the signup form for a new user"""
    form = SignupForm()
    if form.validate_on_submit():
        print("Form validated and submitted")

        # Extract form data correctly using form object
        email = form.email.data
        password = form.password.data
        username = form.username.data


        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash("User already exists", "error")
            return redirect(url_for('auth.signup')), 400

        
        # Create a new user and save to the database
        user = User(username=form.username.data, email=email, password=hash_password(password))  # Assuming `hash_password` hashes the password

        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))

    if form.errors:
        print("Form validation errors:", form.errors)

    return render_template('auth/signup.html', title='Signup', form=form)  # Pass form object, not string


@auth_bp.route('/logout')
def logout():
    """ Handles the logout """
    logout_user()
    return redirect(url_for('auth.login'))