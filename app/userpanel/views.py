from flask import render_template, redirect, flash, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import or_, desc, asc, func
from . import userpanel
from .forms import LoginForm, RegisterForm, CustomerEditForm
from ..database import db
from ..models.Userpanel import Customer, CustomerCalculation, CustomerActivity
from ..helpers.no_cache import nocache
from ..helpers.file_helper import save_picture


@userpanel.route('/userpanel/login', methods=['GET', 'POST'])
@nocache
def login():
    form = LoginForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('userpanel.dashboard'))

    if form.validate_on_submit():
        customer = Customer.query.filter(
            or_(Customer.login == form.login_or_email.data, Customer.email == form.login_or_email.data)).first()
        if customer and check_password_hash(customer.password, form.password.data):
            login_user(customer, remember=form.remember.data)
            return redirect(url_for('userpanel.dashboard'))

        flash("Invalid username or password", 'danger')

    return render_template('userpanel/login.html', title="Login to your account", form=form)


@userpanel.route('/userpanel/logout')
@login_required
@nocache
def logout():
    logout_user()
    return redirect(url_for('userpanel.login'))


@userpanel.route('/userpanel/register', methods=['GET', 'POST'])
@nocache
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_customer = Customer(first_name=form.first_name.data, last_name=form.last_name.data,
                                login=form.login.data, email=form.email.data, password=hashed_password)
        db.session.add(new_customer)
        db.session.commit()

        login_user(new_customer)

        return redirect(url_for('userpanel.dashboard'))

    return render_template('userpanel/register.html', title="Register for an account", form=form)


@userpanel.route('/userpanel/', methods=['GET'], strict_slashes=False)
@login_required
@nocache
def userpanel_view():
    return redirect(url_for('userpanel.dashboard'))


@userpanel.route('/userpanel/dashboard', methods=['GET'])
@login_required
@nocache
def dashboard():
    activity = CustomerActivity.query.with_entities(CustomerActivity.id, CustomerActivity.customer_id,
                                                    CustomerActivity.module_name, CustomerActivity.url,
                                                    func.count(CustomerActivity.url).label('count')) \
        .filter_by(customer=current_user) \
        .group_by(CustomerActivity.url).all()

    statistics = {}
    statistics['total_calculations'] = CustomerCalculation.query.filter_by(customer=current_user).count()
    statistics['total_visits'] = CustomerActivity.query.filter_by(customer=current_user).count()
    return render_template('userpanel/dashboard.html', title="Dashboard", user=current_user.login, activity=activity,
                           statistics=statistics)


@userpanel.route('/userpanel/editprofile', methods=['GET', 'POST'])
@login_required
@nocache
def edit_profile():
    customer_id = current_user.id

    profile = Customer.query.get_or_404(customer_id)
    form = CustomerEditForm(obj=profile)

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            profile.profile_pic = picture_file

        if form.password.data:
            profile.password = generate_password_hash(form.password.data, method='sha256')

        profile.first_name = form.first_name.data
        profile.last_name = form.last_name.data

        db.session.add(profile)
        db.session.commit()

        flash('You have successfully edited the profile.', 'success')

        return redirect(url_for('userpanel.edit_profile'))

    profile_pic = url_for('static', filename='uploads/profile_pics/' + current_user.profile_pic)

    return render_template('userpanel/edit_profile.html', form=form, profile_pic=profile_pic)


@userpanel.route('/userpanel/calculations', methods=['GET'])
@login_required
@nocache
def calculations_all():
    query = request.args.get('query')
    order_by = request.args.get('order_by', "created_at")
    sort_by = request.args.get('sort_by')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if query:
        return redirect(
            url_for('userpanel.calculations_search', query=query, order_by=order_by, sort_by=sort_by, page=page))

    if sort_by == "desc":
        calculations = CustomerCalculation.query.filter_by(customer=current_user) \
            .order_by(desc(order_by)) \
            .paginate(page=page, per_page=per_page)
    elif sort_by == "asc":
        calculations = CustomerCalculation.query.filter_by(customer=current_user) \
            .order_by(asc(order_by)) \
            .paginate(page=page, per_page=per_page)
    else:
        calculations = CustomerCalculation.query.filter_by(customer=current_user) \
            .order_by(desc(order_by)) \
            .paginate(page=page, per_page=per_page)

    return render_template('userpanel/calculations.html', calculations=calculations)


@userpanel.route('/userpanel/calculations/search', methods=['GET'])
@login_required
@nocache
def calculations_search():
    query = request.args.get('query')
    order_by = request.args.get('order_by', "created_at")
    sort_by = request.args.get('sort_by')
    page = request.args.get('page', 1, type=int)
    per_page = 5
    if sort_by == "desc":
        calculations = CustomerCalculation.query.filter(CustomerCalculation.title.like(f'%{query}%')) \
            .filter(CustomerCalculation.customer == current_user) \
            .order_by(desc(order_by)) \
            .paginate(page=page, per_page=per_page)
    elif sort_by == "asc":
        calculations = CustomerCalculation.query.filter(CustomerCalculation.title.like(f'%{query}%')) \
            .filter(CustomerCalculation.customer == current_user) \
            .order_by(asc(order_by)) \
            .paginate(page=page, per_page=per_page)
    else:
        calculations = CustomerCalculation.query.filter(CustomerCalculation.title.like(f'%{query}%')) \
            .filter(CustomerCalculation.customer == current_user) \
            .order_by(desc(order_by)) \
            .paginate(page=page, per_page=per_page)

    return render_template('userpanel/calculations.html', calculations=calculations)


@userpanel.route('/userpanel/calculations/delete/<int:calculation_id>')
@login_required
@nocache
def calculation_delete(calculation_id):
    calculation = CustomerCalculation.query.filter_by(id=calculation_id).first()
    db.session.delete(calculation)
    db.session.commit()

    return redirect(url_for('userpanel.calculations_all'))


@userpanel.route('/userpanel/calculations/<int:calculation_id>')
@login_required
@nocache
def calculation_detail(calculation_id):
    calculation = CustomerCalculation.query.filter_by(id=calculation_id).first()

    return render_template('userpanel/calculation_detail.html', calculation=calculation)
