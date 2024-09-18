from flask import Flask, Blueprint, request, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_login import login_required 
from app.models import Products

shop_bp = Blueprint('shop', __name__)

cart = []

@shop_bp.route('/search', methods=['GET', 'POST'])
def search():
    """ Handles the search button """
    if request.method == 'POST':
        search_item = request.form.get('search_item', '')
        # This querys the database to check products that matches the search
        product = Products.query.filter(product.name.ilike(f'%{search_item}%')).all()
        return render_template('search_result.html', product=products, search_item=search_item)
    else:
        flash()
    return redirect(url_for('products'))


@shop_bp.route('/products')
def products():
    """ Handlesl the shopping/product page """
    all_product = Products.query.all() # Fetches all the product from the database
    return render_template('shop.html', all_product=all_product)


@shop_bp.route('/add_to_cart/int:product_id', methods=['POST'])
def add_to_cart():
    """ Handles the ordered product """
    product = Products.query.get_or_404(product_id)

    if product.quantity > 0:
        # cart.append(product)
        product.quantity -= 1 # Reduce product quantity by 1 after orderd
        db.session.commit()
        flash('product added to cart!', 'success')
    else:
        flash('sorry this product is sold out', 'danger')

    return redirect(url_for('products'))



@shop_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    """ Handles the checkout after a successful order """
    total_amount = sum(item.price for item in cart) # This calculates the total amount of the items ordered
    
    # Proceed with payment or clear the cart
    cart.clear
    flash(f'checkout successfully! The total amount of your other is ${total_amount:.2f}.', 'success')
    return redirect(url_for('products'))