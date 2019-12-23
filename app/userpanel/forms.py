from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from flask_wtf.file import FileField
from wtforms import BooleanField
from wtforms import DateTimeField
from wtforms import FloatField
from wtforms import HiddenField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length
from wtforms.validators import ValidationError

from app.userpanel.models import Customer
from app.userpanel.models import NCBIMail
from app.userpanel.models import NCBIMailPackage


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
        for instance_attribute in dir(form):
            if instance_attribute.startswith("model"):
                delattr(form, instance_attribute)

        for key in data:
            setattr(form, f"model_{key}", FloatField(key))


class NCBIPackageForm(FlaskForm):
    id = HiddenField()
    name = StringField('Package name:', validators=[DataRequired()])
    comment = TextAreaField('Package comment:')
    was_sent = BooleanField('Was sent:')


def get_mail_package_choices():
    ncbi_packages = NCBIMailPackage.query.filter_by(was_sent=False).all()

    return [(package.id, package.name) for package in ncbi_packages]


class NCBIMailFrom(FlaskForm):
    id = HiddenField()
    email = EmailField('Email:', validators=[DataRequired(), Email()])
    ncbi_publication_url = StringField('NCBI publication url:')
    publication_id = StringField('NCBI publication id:')
    mail_package = SelectField('Package:', coerce=int)

    def validate_email(self, email):
        email = NCBIMail.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError(
                f'This e-mail is already present in our db in the package: {email.ncbi_mail_packages.name}'
            )
