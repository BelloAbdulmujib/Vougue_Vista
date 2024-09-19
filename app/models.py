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

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

# Defines the admin model
class Admin(db.Model):
    """ This is admin class in the model """
    id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<Admin{self.name}>'

    def is_active(self):
        """Override is_active for Flask-Login."""
        return self.active


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
class Order(db.Model):
    """ Stores the ordered products """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Cash on Delivery", nullable=False)
    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f"Order(id={self.id}, user_id={self.order_id}, total_amount={self.total_amount}, status={self.status}, items={self.items})"

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    
    product = db.relationship('Products', backref='cart_items')

    def __repr__(self):
        return f'<CartItem {self.id}, Product {self.product_id}>'

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f"OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity}, unit_price={self.unit_price})"
