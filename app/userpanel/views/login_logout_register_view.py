from flask import abort
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from is_safe_url import is_safe_url
from sqlalchemy import or_
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.database import db
from app.userpanel.decorators import nocache
from app.userpanel.forms import LoginForm
from app.userpanel.forms import RegisterForm
from app.userpanel.models import Customer
from app.userpanel.views import userpanel
from config import ALLOWED_HOSTS


@userpanel.route('/login', methods=['GET', 'POST'])
def login_view():
    form = LoginForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('userpanel.dashboard_view'))

    if form.validate_on_submit():
        customer = Customer.query.filter(
            or_(Customer.login == form.login_or_email.data, Customer.email == form.login_or_email.data)
        ).first()

        if customer and check_password_hash(customer.password, form.password.data):
            login_user(customer, remember=form.remember.data)

            next = request.args.get('next')
            if next and not is_safe_url(next, ALLOWED_HOSTS):
                return abort(400)

            return redirect(next or url_for('userpanel.dashboard_view'))

        flash("Invalid username or password", 'danger')

    return render_template('userpanel/customers/login.html', title="Login to your account", form=form)


@userpanel.route('/logout')
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('userpanel.login_view'))


@userpanel.route('/register', methods=['GET', 'POST'])
@nocache
def register_view():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_customer = Customer(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            login=form.login.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(new_customer)
        db.session.commit()

        login_user(new_customer)

        next = request.args.get('next')
        if next and not is_safe_url(next, ALLOWED_HOSTS):
            return abort(400)

        return redirect(next or url_for('userpanel.dashboard_view'))

    return render_template('userpanel/customers/register.html', title="Register for an account", form=form)
