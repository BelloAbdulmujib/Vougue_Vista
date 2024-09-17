import pytest
from app import db
from app.models import User, Admin, Products, Orders
from werkzeug.security import generate_password_hash, check_password_hash

def test_user_model(init_database):
    """ Test User model creation and methods """
    user = User(username='testuser', email='test@example.com', password=generate_password_hash('password'))
    db.session.add(user)
    db.session.commit()

    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.check_password('password') is True
    assert user.check_password('wrongpassword') is False

def test_admin_model(init_database):
    """ Test Admin model creation """
    admin = Admin(username='adminuser', email='admin@example.com', password=generate_password_hash('adminpassword'))
    db.session.add(admin)
    db.session.commit()

    assert admin.username == 'adminuser'
    assert admin.email == 'admin@example.com'

def test_products_model(init_database):
    """ Test Products model creation """
    product = Products(name='Test Product', description='This is a test product', quantity=10, image='test_image.jpg')
    db.session.add(product)
    db.session.commit()

    assert product.name == 'Test Product'
    assert product.description == 'This is a test product'
    assert product.quantity == 10
    assert product.image == 'test_image.jpg'

def test_orders_model(init_database):
    """ Test Orders model creation """
    order = Orders(name='Test Order', description='This is a test order', quantity=5, image='order_image.jpg')
    db.session.add(order)
    db.session.commit()

    assert order.name == 'Test Order'
    assert order.description == 'This is a test order'
    assert order.quantity == 5
    assert order.image == 'order_image.jpg'
