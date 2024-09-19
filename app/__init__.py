from flask import Flask
from flask_mail import Mail
from config import Config

from extensions import db, login
from app import models

from app.routes.auth import auth_bp
from app.routes.shop import shop_bp
from app.routes.payment import payment_bp
from app.routes.admin import admin_bp
from app.routes.landing import landing_bp
from app.routes.admin_data import admin_data_bp
from flask_wtf.csrf import CSRFProtect
import os


app = Flask(__name__)

UPLOAD_FOLDER = './uploads'

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['ALLOWED_EXTENSIONS'] = {'jpeg', 'png', 'jpg'}
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # The folder where the uploads will be saved
    app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024 # limit upload size 3MB
    
    
    db.init_app(app)
    login.init_app(app)

        # This import the routes and models
    app.register_blueprint(auth_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(landing_bp)
    app.register_blueprint(admin_data_bp)

    with app.app_context():
        db.create_all() 

    return app