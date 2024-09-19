from flask import Flask
from config import Config
from extensions import db, login
from app.models import User, AdminModel, Products, Order, Cart
from app import models
from app.routes.auth import auth_bp
from app.routes.shop import shop_bp
from app.routes.payment import payment_bp
# from app.routes.admin import admin_bp
from app.routes.landing import landing_bp
from app.routes.admin_data import admin_data_bp
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.admin_views import ProductAdmin
import os

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['ALLOWED_EXTENSIONS'] = {'jpeg', 'png', 'jpg'}
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # The folder where the uploads will be saved
    app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024 # limit upload size 3MB

    db.init_app(app)
    login.init_app(app)

    # Add views for your models
    admin = Admin(app, name='Admin Dashboard', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(AdminModel, db.session))
    admin.add_view(ProductAdmin(Products, db.session))
    admin.add_view(ModelView(Order, db.session))

        # This import the routes and models
    app.register_blueprint(auth_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(payment_bp)
    # app.register_blueprint(admin_bp)
    app.register_blueprint(landing_bp)
    app.register_blueprint(admin_data_bp)

    with app.app_context():
        db.create_all() 

    return app