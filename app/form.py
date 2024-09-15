from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
class LoginForm(FlaskForm):
    """Handles the login in form details """
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remenber Me')
    submit = SubmitField('login')


class SignupForm(FlaskForm):
    """ Handles the signup form detail """
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('Signup')

    def validate_email(self, email):
        """ email validation before signup """
        email = User.query.filter_by(email=email.data).first()
        if User is not None:
            raise ValidationError('Email already exist, please use a different email address.')