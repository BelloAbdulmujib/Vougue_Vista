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

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def is_active(self):
        """Override is_active for Flask-Login."""
        return self.active

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
    price = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
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
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Orders{self.name}>'

# Defines the cart model
class Cart(db.Model):
    """ Stores the ordered products """
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Numeric(10, 2), default=0.00)
    items = db.relationship('CartItem', backref='cart', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f'<Cart{self.id}>'

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id', ondelete="CASCADE"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)  # quantity * unit_price

    def __repr__(self):
        return f'<CartItem {self.id}, Product {self.product_id}>'


