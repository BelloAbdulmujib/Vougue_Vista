from flask import Flask, Blueprint, request, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_login import login_required, current_user
from app.models import Products, Cart
from app import db

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
@login_required
def add_to_cart():
    """ Handles the ordered product """
    product_id = request.form.get('product_id')
    product_price = request.form.get('price')
    product = Products.query.get_or_404(product_id)
    user_id = current_user.id
    
    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(
            user_id=user_id,
            product_id=product_id,
            quantity=1,
            unit_price=product_price,
            image=product.image
        )
        db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for('shop.products'))



@shop_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    """ Handles the checkout after a successful order """
    total_amount = sum(item.price for item in cart) # This calculates the total amount of the items ordered
    
    # Proceed with payment or clear the cart
    cart.clear
    flash(f'checkout successfully! The total amount of your other is ${total_amount:.2f}.', 'success')
    return redirect(url_for('products'))

@shop_bp.route('/cart')
@login_required
def cart():
    user_id = current_user.id
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    total_price = sum(item.unit_price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@shop_bp.route('/edit_cart/<int:cart_item_id>', methods=['POST'])
@login_required
def edit_cart(cart_item_id):
    """Handles updating the quantity of an item in the cart."""
    new_quantity = request.form.get('quantity', type=int)

    cart_item = Cart.query.filter_by(id=cart_item_id, user_id=current_user.id).first()

    if cart_item:
        # Update the quantity if the item exists in the user's cart
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            db.session.commit()
            flash('Cart updated successfully!', 'success')
        else:
            db.session.delete(cart_item)
            db.session.commit()
    else:
        flash('Item not found in cart.', 'error')
    
    return redirect(url_for('shop.cart'))

@shop_bp.route('/delete_cart/<int:cart_item_id>', methods=['POST'])
@login_required
def delete_cart(cart_item_id):
    """Handles removing an item from the cart."""
    cart_item = Cart.query.filter_by(id=cart_item_id, user_id=current_user.id).first()
    
    if cart_item:
        # Remove the item from the cart
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart successfully!', 'success')
    else:
        flash('Item not found in cart.', 'error')
    
    return redirect(url_for('shop.cart'))