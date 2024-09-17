from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Configuration for SQLAlchemy
class Config:
    SECRET_KEY = 'your secretkey'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'VogueVista.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///VogueVista.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'

# Configuration for testing environment
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for faster tests
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing forms
    DEBUG = True
