from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, Length
from app.models import User
class LoginForm(FlaskForm):
    """Handles the login in form details """
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remenber Me')
    submit = SubmitField('login')


class SignupForm(FlaskForm):
    """ Handles the signup form detail """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    # password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('Signup')

    def validate_email(self, email):
        """ email validation before signup """
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Email already exist, please use a different email address.')