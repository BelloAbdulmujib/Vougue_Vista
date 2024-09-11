from flask import Flask, Blueprint
from paypalrestsdk import Payment
from flask import request, jsonify, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import stripe


payment_bp = Blueprint('payment', __name__)

# The cart is a list of products
cart = []  # This should be populated based on the user's session or database


@payment_bp.route('/pay_paypal', methods=['POST'])
def pay_paypal():
    # Calculate the total amount from the cart
    total_amount = sum(item.price for item in cart)

    # Get the user's phone number from the form
    phone_number = request.form.get('phone_number')

    # Create a PayPal payment object
    payment = Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [{
            "amount": {"total": f"{total_amount:.2f}", "currency": "USD"},
            "description": "Your purchase description",
            "item_list": {
                "items": [{"name": item.name, "price": f"{item.price:.2f}", "currency": "USD", "quantity": 1} for item in cart]
            },
            "payee": {
                "phone": {"number": phone_number}
            }}],
        "redirect_urls": {
            "return_url": url_for('execute_payment', _external=True),
            "cancel_url": url_for('cancel_payment', _external=True)}}
    )

    if payment.create():
        return jsonify({"paymentID": payment.id})
    else:
        return jsonify({"error": payment.error})


def send_confirmation_email(payment, is_admin=False):
    # Admin email address
    admin_email = 'admin@example.com'

    # User's email address
    user_email = payment['payer']['payer_info']['email']

    # Order details
    order_details = "\n".join([f"{item.name}: ${item.price:.2f} USD" for item in cart])

    # Adjust order details for Stripe payments in NGN
    if payment.currency == 'ngn':
        order_details = "\n".join([f"{item.name}: ₦{(item.price * USD_TO_NGN_CONVERSION_RATE):.2f} NGN" for item in cart])

    # Common email subject
    subject = "Order Confirmation"

    # Email body
    if is_admin:
        body = (f"A new order has been placed by {user_email}.\n\n"
                f"Order Details:\n{order_details}\n"
                f"Total: {payment['transactions'][0]['amount']['total']} {payment.currency.upper()}\n\n"
                f"Please proceed with the order delivery.\n\nBest regards,\nYour E-commerce Platform")
    else:
        body = (f"Thank you for your purchase! Your order is successful.\n\n"
                f"Order Details:\n{order_details}\n"
                f"Total: {payment['transactions'][0]['amount']['total']} {payment.currency.upper()}\n\n"
                f"We will contact you at {payment['transactions'][0]['payee']['phone']['number']} for any further communication.\n\n"
                f"Best regards,\nYour E-commerce Platform")

    msg = MIMEMultipart()
    msg['From'] = 'your_email@example.com'
    msg['To'] = admin_email if is_admin else user_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login('acleff73@gmail.com', 'your_email_password')
    text = msg.as_string()
    server.sendmail('acleff73@gmail.com', admin_email if is_admin else user_email, text)
    server.quit()


@payment_bp.route('/payment/execute', methods=['POST'])
def execute_payment():
    payment_id = request.form.get('paymentID')
    payer_id = request.form.get('payerID')

    payment = Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Send an email confirmation to the user
        send_confirmation_email(payment)

        # Send an email notification to the admin
        send_confirmation_email(payment, is_admin=True)

        # Display a success message to the user
        flash('Payment successful! An email confirmation has been sent to you.', 'success')
        return redirect(url_for('products'))
    else:
        flash('Payment failed. Please try again.', 'danger')
        return redirect(url_for('products'))


stripe.api_key = 'your_stripe_secret_key'

# Example conversion rate (update with real data)
USD_TO_NGN_CONVERSION_RATE = 1550  # Example rate

@payment_bp.route('/pay_with_card', methods=['POST'])
def pay_with_card():
    try:
        # Calculate the total amount in NGN
        total_amount_usd = sum(item.price for item in cart)
        total_amount_ngn = total_amount_usd * USD_TO_NGN_CONVERSION_RATE

        charge = stripe.Charge.create(
            amount=int(total_amount_ngn),  # Stripe expects amount in kobo (1 NGN = 100 kobo)
            currency='ngn',
            source=request.form['stripeToken'],
            description='Your purchase description',
        )

        # Send an email confirmation
        send_confirmation_email(charge)
        
        flash('Payment successful! An email confirmation has been sent to you.', 'success')
        return redirect(url_for('products'))
    except stripe.error.StripeError as e:
        flash(f'Payment failed: {e.user_message}', 'danger')
        return redirect(url_for('products'))
