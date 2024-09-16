import pytest
from flask import url_for
from app.form import LoginForm
from app.models import User
from app import db
from werkzeug.security import generate_password_hash

def test_login_form_valid(client, init_database):
    """ Test valid login """
    # Create a test user
    user = User(email='test@example.com', password=generate_password_hash('password'))
    db.session.add(user)
    db.session.commit()

    # Test the login form
    response = client.post(url_for('auth.login'), data=dict(
        email='test@example.com',
        password='password',
        remember_me=True
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b'Welcome' in response.data  # Adjust based on actual login success message

def test_login_form_invalid(client):
    """ Test invalid login """
    response = client.post(url_for('auth.login'), data=dict(
        email='invalid@example.com',
        password='wrongpassword'
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid email or password' in response.data  # Adjust based on actual error message
