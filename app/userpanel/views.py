from flask import render_template, redirect, flash, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import or_, desc, asc, func

from app.userpanel import userpanel
from app.userpanel.forms import LoginForm
from app.userpanel.forms import RegisterForm
from app.userpanel.forms import CustomerEditForm
from app.userpanel.forms import PageEditForm
from app.userpanel.forms import AdminCustomerEditForm

from app.userpanel.models import Customer
from app.userpanel.models import CustomerActivity
from app.userpanel.models import Page

from app.customer_calculation.models import CustomerCalculation

from app.database import db
from app.helpers.no_cache import nocache
from app.helpers.file_helper import save_picture


@userpanel.route('/userpanel/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('userpanel.dashboard_view'))

    if form.validate_on_submit():
        customer = Customer.query.filter(
            or_(Customer.login == form.login_or_email.data, Customer.email == form.login_or_email.data)).first()
        if customer and check_password_hash(customer.password, form.password.data):
            login_user(customer, remember=form.remember.data)
            return redirect(url_for('userpanel.dashboard_view'))

        flash("Invalid username or password", 'danger')

    return render_template('userpanel/customers/login.html', title="Login to your account", form=form)


@userpanel.route('/userpanel/logout')
@login_required
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

        return redirect(url_for('userpanel.dashboard_view'))

    return render_template('userpanel/customers/register.html', title="Register for an account", form=form)


@userpanel.route('/userpanel/', methods=['GET'], strict_slashes=False)
@login_required
def userpanel_view():
    return redirect(url_for('userpanel.dashboard_view'))


@userpanel.route('/userpanel/dashboard', methods=['GET'])
@login_required
def dashboard_view():
    activity = CustomerActivity.query.with_entities(CustomerActivity.url, CustomerActivity.module_name,
                                                    func.count(CustomerActivity.url).label('count')) \
        .filter_by(customer=current_user) \
        .group_by(CustomerActivity.url, CustomerActivity.module_name).all()

    statistics = {}
    statistics['total_calculations'] = CustomerCalculation.query.filter_by(customer=current_user).count()
    statistics['total_visits'] = CustomerActivity.query.filter_by(customer=current_user).count()
    return render_template('userpanel/dashboard.html', title="Dashboard", user=current_user.login, activity=activity,
                           statistics=statistics)


@userpanel.route('/userpanel/editprofile', methods=['GET', 'POST'])
@login_required
def edit_profile_view():
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

        return redirect(url_for('userpanel.edit_profile_view'))

    profile_pic = url_for('static', filename='uploads/profile_pics/' + current_user.profile_pic)

    return render_template('userpanel/customers/customer_edit_profile.html', form=form, profile_pic=profile_pic)


@userpanel.route('/userpanel/calculations', methods=['GET'])
@login_required
def calculations_list_view():
    query = request.args.get('query')
    order_by = request.args.get('order_by', "created_at")
    sort_by = request.args.get('sort_by')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if query:
        return redirect(
            url_for('userpanel.calculations_search_view', query=query, order_by=order_by, sort_by=sort_by, page=page))

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

    return render_template('userpanel/calculations/calculations.html', calculations=calculations)


@userpanel.route('/userpanel/calculations/search', methods=['GET'])
@login_required
def calculations_search_view():
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

    return render_template('userpanel/calculations/calculations.html', calculations=calculations)


@userpanel.route('/userpanel/calculations/delete/<int:calculation_id>')
@login_required
def calculation_delete_view(calculation_id):
    calculation = CustomerCalculation.query.filter_by(id=calculation_id).first()
    db.session.delete(calculation)
    db.session.commit()

    return redirect(url_for('userpanel.calculations_list_view'))


@userpanel.route('/userpanel/calculations/<int:calculation_id>')
@login_required
def calculation_details_view(calculation_id):
    calculation = CustomerCalculation.query.filter_by(id=calculation_id).first()

    return render_template('userpanel/calculations/calculation_details.html', calculation=calculation)


@userpanel.route('/userpanel/pages')
@login_required
def pages_list_view():
    pages = Page.query.all()
    return render_template('userpanel/pages/pages.html', pages=pages)


@userpanel.route('/userpanel/pages/<int:page_id>', methods=['GET', 'POST'])
@login_required
def page_details_view(page_id):
    page = Page.query.get_or_404(page_id)
    form = PageEditForm(obj=page)

    if form.validate_on_submit():
        page.name = form.name.data
        page.is_active = form.is_active.data
        page.slug = form.slug.data
        page.seo_title = form.seo_title.data
        page.desc = form.seo_desc.data
        page.seo_keywords = form.seo_keywords.data
        page.text = form.text.data
        page.desc = form.desc.data

        db.session.add(page)
        db.session.commit()

        flash('You have successfully edited the page.', 'success')

        return redirect(url_for('userpanel.page_details_view', page_id=page.id))

    return render_template('userpanel/pages/page_details.html', form=form, page=page)


@userpanel.route('/userpanel/pages/add-page', methods=['GET', 'POST'])
@login_required
def page_add_view():
    form = PageEditForm()

    if form.validate_on_submit():
        page = Page()
        page.name = form.name.data
        page.is_active = form.is_active.data
        page.slug = form.slug.data
        page.seo_title = form.seo_title.data
        page.desc = form.seo_desc.data
        page.seo_keywords = form.seo_keywords.data
        page.text = form.text.data
        page.desc = form.desc.data

        db.session.add(page)
        db.session.commit()

        flash('You have successfully added the page.', 'success')

        return redirect(url_for('userpanel.pages_list_view'))

    return render_template('userpanel/pages/page_add.html', form=form)


@userpanel.route('/userpanel/pages/delete/<int:page_id>')
@login_required
def page_delete_view(page_id):
    page = Page.query.get_or_404(page_id)

    db.session.delete(page)
    db.session.commit()

    flash('You have successfully delete the page - {}.'.format(page.name), 'success')

    return redirect(url_for('userpanel.pages_list_view'))


@userpanel.route('/userpanel/customers/')
@login_required
def customers_list_view():
    customers = Customer.query.all()
    return render_template('userpanel/customers/customers.html', customers=customers)


@userpanel.route('/userpanel/customers/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def customer_details_view(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    form = AdminCustomerEditForm(obj=customer)

    if form.validate_on_submit():
        customer.first_name = form.first_name.data
        customer.last_name = form.last_name.data
        customer.login = form.login.data
        customer.email = form.email.data
        customer.password = form.password.data
        customer.is_superuser = form.is_superuser.data
        customer.created_at = form.created_at.data

        db.session.add(customer)
        db.session.commit()

        flash('You have successfully edited the customer.', 'success')

        return redirect(url_for('userpanel.customer_details_view', customer_id=customer.id))

    return render_template('userpanel/customers/customer_details.html', form=form, customer=customer)


@userpanel.route('/userpanel/customers/delete/<int:customer_id>')
@login_required
def customer_delete_view(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    db.session.delete(customer)
    db.session.commit()

    flash('You have successfully delete the customer - {}.'.format(customer.login), 'success')

    return redirect(url_for('userpanel.customers_list_view'))


@userpanel.context_processor
def inject():
    return {
        'module_desc': Page.query.filter_by(slug=request.path).first()
    }
