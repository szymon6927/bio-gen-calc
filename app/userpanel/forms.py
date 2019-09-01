from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from flask_wtf.file import FileField
from wtforms import BooleanField
from wtforms import DateTimeField
from wtforms import HiddenField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length
from wtforms.validators import ValidationError

from app.userpanel.models import Customer


class LoginForm(FlaskForm):
    login_or_email = StringField('Login or e-mail:', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    first_name = StringField('First name:')
    last_name = StringField('Last name:')
    login = StringField('Login*', validators=[DataRequired(), Length(min=3, max=25)])
    email = EmailField('Email*', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password*',
        validators=[DataRequired(), Length(min=8, max=80), EqualTo('password_confirm', message='Passwords must match')],
    )
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
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    first_name = StringField('First name:', validators=[DataRequired()])
    last_name = StringField('Last name:', validators=[DataRequired()])
    login = StringField('Login*:')
    email = EmailField('Email*:')
    password = PasswordField('New password:', validators=[EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Confirm new password:')

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

    def validate_password(self, password):
        lower_name = self.first_name.data.lower()

        if lower_name in password.data:
            raise ValidationError('Password contain your first name, please change this.')


class PageEditForm(FlaskForm):
    id = HiddenField()
    name = StringField('Page name:', validators=[DataRequired()])
    is_active = BooleanField('Active:')
    slug = StringField('Page slug:')
    seo_title = StringField('SEO title:')
    seo_desc = StringField('SEO description:')
    seo_keywords = StringField('SEO keywords:')
    text = TextAreaField('Page text:')
    desc = TextAreaField('Page description:')


class AdminCustomerEditForm(FlaskForm):
    id = HiddenField()
    first_name = StringField('First name:')
    last_name = StringField('Last name:')
    login = StringField('Login:')
    email = EmailField('Email:')
    password = PasswordField('Password:')
    is_superuser = BooleanField('Super user:')
    created_at = DateTimeField('Created:')


class ModelForm(FlaskForm):
    @staticmethod
    def update_form(form, data):
        for key in data:
            setattr(form, key, StringField(key, validators=[DataRequired()]))
