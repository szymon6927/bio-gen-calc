from flask import render_template, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import and_
from . import userpanel
from .forms import LoginForm, RegisterForm
from ..database import db
from ..models.Userpanel import Customer



@userpanel.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('userpanel.dashboard'))
        
    if form.validate_on_submit():
        customer = Customer.query.filter_by(login=form.login.data).first()
        if customer:
            if check_password_hash(customer.password, form.password.data):
                login_user(customer, remember=form.remember.data)
                return redirect(url_for('userpanel.dashboard'))

        flash("Invalid username or password", 'danger')

    return render_template('userpanel/login.html', title="Login", form=form)


@userpanel.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.homepage'))

@userpanel.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        customer = Customer.query.filter(and_(Customer.login == form.login.data, Customer.email == form.email.data))

        if customer:
            flash("User with this login and email already exist", 'danger')
            return redirect(url_for('userpanel.register'))
        else:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_customer = Customer(first_name=form.first_name.data, last_name=form.last_name.data, login=form.login.data, email=form.email.data, password=hashed_password)
            db.session.add(new_customer)
            db.session.commit()

        return redirect(url_for('userpanel.dashboard'))

    return render_template('userpanel/register.html', title="Register", form=form)


@userpanel.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('userpanel/dashboard.html', title="Dashboard", user=current_user.login)