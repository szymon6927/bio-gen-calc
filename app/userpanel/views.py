from flask import render_template, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from . import userpanel
from .forms import LoginForm, RegisterForm
from ..database import db
from ..models.Userpanel import Customer



@userpanel.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('userpanel/login.html', title="Login", form=form)


@userpanel.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_customer = Customer(first_name=form.first_name.data, last_name=form.last_name.data, login=form.login.data, email=form.email.data, password=hashed_password)
        db.session.add(new_customer)
        db.session.commit()

        return redirect(url_for('userpanel.dashboard'))

    return render_template('userpanel/register.html', title="Register", form=form)


@userpanel.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('userpanel/dashboard.html', title="Dashboard")