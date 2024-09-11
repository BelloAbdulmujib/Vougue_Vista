from flask import Flask, render_template, Blueprint


landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/')
def home():
    """ Handles the landing page """
    return render_template('landing.html', title='Landing')