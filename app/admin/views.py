import os

from flask import url_for, redirect, request, jsonify

from wtforms import form, validators, fields, widgets

import flask_admin as admin
import flask_login as login

from flask_admin import BaseView, helpers, expose

from ..database import db
from .models import Page, User

from flask_admin.contrib import sqla

from werkzeug.security import generate_password_hash, check_password_hash


class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        # add WYSIWYG class to existing classes
        existing_classes = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % (existing_classes, "ckeditor")
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password_hash, self.password.data):
            # to compare plain text passwords use
            # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()


class RegistrationForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    email = fields.StringField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if db.session.query(User).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated


def get_static_abs_path():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.dirname(current_dir)

    abs_static_path = os.path.join(parent_dir, 'static', 'uploads')
    static_path = os.path.join('/', 'static', 'uploads')
    return {'abs_static_path': abs_static_path, 'static_path': static_path}


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):
    paths = get_static_abs_path()
    UPLOADED_PATH = paths.get('abs_static_path')

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            user.password_hash = generate_password_hash(form.password.data)

            db.session.add(user)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))

    @expose('/upload/', methods=['POST'])
    def upload(self):
        f = request.files.get('upload')
        extension = f.filename.split('.')[1].lower()
        if extension not in ['jpg', 'gif', 'png', 'jpeg']:
            return jsonify(uploaded=0, error={'message': 'Image only!'})

        f.save(os.path.join(self.UPLOADED_PATH, f.filename))

        url = os.path.join(self.paths.get('static_path'), f.filename)
        response = {"uploaded": 1, "fileName": f.filename, "url": url}
        return jsonify(response)


class PageAdmin(sqla.ModelView):
    form_overrides = dict(text=CKTextAreaField, desc=CKTextAreaField)
    column_exclude_list = ('text', 'desc')
    create_template = 'admin_overwrite/create.html'
    edit_template = 'admin_overwrite/edit.html'


def run_admin():
    admin_panel = admin.Admin(name="Gene Calc - Admin Panel", index_view=MyAdminIndexView(),
                              base_template='admin_overwrite/layout.html', template_mode='bootstrap4')

    admin_panel.add_view(MyModelView(User, db.session))
    admin_panel.add_view(PageAdmin(Page, db.session))

    return admin_panel
