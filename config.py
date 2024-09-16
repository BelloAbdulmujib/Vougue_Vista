from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Configuration for SQLAlchemy
class Config:
    SECRET_KEY = 'your secretkey'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'VogueVista.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///VogueVista.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'