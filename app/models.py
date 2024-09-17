from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from sqlalchemy import Column, String, Float
from werkzeug.security import generate_password_hash, check_password_hash


# Defines the user's model
class User(db.Model):
    """ The user class in the database """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_user_id():
        return str(self.id)

    def __repr__(self):
        return f'<User {self.username}>'

# Defines the admin model
class Admin(db.Model):
    """ This is admin class in the model """
    id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Admin{self.name}>'


# Defines the products model
class Products(db.Model):
    """ New added/upload products in the database """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    image = db.Column(db.String(100), nullable=False)
       
    def __repr__(self):
        return f'<Products{self.name}>'
    

# Defines the orders model
class Orders(db.Model):
    """ Stores the ordered products """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Orders{self.name}>'
