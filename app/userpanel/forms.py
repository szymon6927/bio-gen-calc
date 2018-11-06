from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from ..models.Userpanel import Customer


class LoginForm(FlaskForm):
    login = StringField('Login:', validators=[DataRequired(), Length(min=4, max=15)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    first_name = StringField('First name:')
    last_name = StringField('Last name:')
    login = StringField('Login*', validators=[DataRequired(), Length(min=3, max=25)])
    email = EmailField('Email*', validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[DataRequired(), Length(min=8, max=80),
                                                      EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Confirm password*', validators=[DataRequired()])


    def validate_login(self, login):
        customer = Customer.query.filter_by(login=login.data).first()
        if customer:
            raise ValidationError('That login is taken. Please choose a different one.')

    def validate_email(self, email):
        customer = Customer.query.filter_by(email=email.data).first()
        if customer:
            raise ValidationError('That email is taken. Please choose a different one.')


class CustomerEditForm(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    first_name = StringField('First name:')
    last_name = StringField('Last name:')
    login = StringField('Login*')
    email = EmailField('Email*')

    def validate_login(self, login):
        if login.data != current_user.login:
            customer = Customer.query.filter_by(login=login.data).first()
            if customer:
                raise ValidationError('You can not change profile login.')

    def validate_email(self, email):
        if email.data != current_user.email:
            customer = Customer.query.filter_by(email=email.data).first()
            if customer:
                raise ValidationError('You can not change profile email.')
