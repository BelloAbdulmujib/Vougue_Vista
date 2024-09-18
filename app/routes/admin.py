from flask import Flask, Blueprint, render_template, request, url_for, redirect, flash, current_app
from flask_sqlalchemy import SQLAlchemy
from app.models import Products
from app import db
import os

app = Flask(__name__)

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin():
    """ Handels redirection to the admin page """
    return render_template('admin.html', tittle='admin')


@admin_bp.route('/admin/add_product', methods=['POST'])
def add_product():
    """ Handles the route for updating/adding a product """
    # baydre test
    product_dir = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(product_dir):
        os.makedir(product_dir)
    
    product_name = request.form['product_name']
    print(product_name)
    price = request.form['price']
    description = request.form['description']
    quantity = request.form['quantity']

    # Handles the file upload

    image = request.files['image']
    if image:
        image_filename = image.filename

    image.save(os.path.join(app.config['UPLOAD_FOLDER']. image_filename))

# Creating instance for the new product
    new_product = Products(
        name=product_name,
        price=price,
        description=description,
        quantity=quantity,
        image=image_filename
    )

    # Adding the new products to the database
    db.session.add(new_product)
    db.session.commit()

    flash('product added successfully!', 'success')
    return redirect(url_for('admin'))


@admin_bp.route('/admin/remove_product/<int:product_id>', methods=['POST'])
def remove_product(product_id):
    """ Handles the route to remove a product """
    product = product.query.get_or_404(product_id)
    db.Session.delete(product)
    db.session.commit

    flash('product removed successfully!', 'success')
    return redirect(url_for('admin'))