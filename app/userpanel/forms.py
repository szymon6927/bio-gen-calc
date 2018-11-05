from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    login = StringField('Login:', validators=[DataRequired(), Length(min=4, max=15)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    first_name = StringField('First name:')
    last_name = StringField('Last name:')
    login = StringField('Login*', validators=[DataRequired(), Length(min=3, max=25)])
    email = EmailField('Email*', validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[DataRequired(), Length(min=8, max=80), EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Confirm password*', validators=[DataRequired()])