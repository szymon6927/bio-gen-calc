import os

from flask import url_for, redirect, request, jsonify, flash

from flask_admin import AdminIndexView, Admin, expose
from flask_admin.contrib import sqla

from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from .utils import get_static_abs_path
from .forms import LoginForm, CKTextAreaField
from ..database import db
from ..models.Admin import Page, User
from ..helpers.no_cache import nocache


# Create customized model view class
class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def on_model_change(self, form, model, is_created):
        model.password_hash = generate_password_hash(model.password_hash, method='sha256')


class GeneAdminIndexView(AdminIndexView):
    paths = get_static_abs_path()
    UPLOADED_PATH = paths.get('abs_static_path')

    @expose('/')
    @nocache
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))

        return super(GeneAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    @nocache
    def login_view(self):
        form = LoginForm()
        if current_user.is_authenticated:
            return redirect(url_for('user.index'))

        if form.validate_on_submit():
            user = User.query.filter_by(login=form.login.data).first()

            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('.index'))
            flash("Invalid username or password", 'danger')

        self._template_args['form'] = form
        return super(GeneAdminIndexView, self).index()

    @expose('/logout/')
    @nocache
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))

    @expose('/upload/', methods=['POST'])
    @nocache
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
    admin_panel = Admin(name="Gene Calc - Admin Panel", index_view=GeneAdminIndexView(),
                        base_template='admin_overwrite/layout.html', template_mode='bootstrap4')

    admin_panel.add_view(MyModelView(User, db.session))
    admin_panel.add_view(PageAdmin(Page, db.session))

    return admin_panel
