from flask import Blueprint
from flask import abort
from flask import flash
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from is_safe_url import is_safe_url
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import or_
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.apmc.config import APMC_REPORTS_UPLOAD_PATH
from app.apmc.ds.report.report_generator import ReportGenerator
from app.apmc.models import APMCData
from app.clients.slack_client import SlackNotification
from app.customer_calculation.models import CustomerCalculation
from app.database import db
from app.helpers.file_helper import remove_file
from app.helpers.file_helper import save_picture
from app.userpanel.decorators import nocache
from app.userpanel.decorators import superuser_required
from app.userpanel.forms import AdminCustomerEditForm
from app.userpanel.forms import CustomerEditForm
from app.userpanel.forms import LoginForm
from app.userpanel.forms import ModelForm
from app.userpanel.forms import PageEditForm
from app.userpanel.forms import RegisterForm
from app.userpanel.models import Calculation
from app.userpanel.models import Customer
from app.userpanel.models import CustomerActivity
from app.userpanel.models import Page
from app.userpanel.services import APMCUserPanelService
from config import ALLOWED_HOSTS

slack_notification = SlackNotification()
userpanel = Blueprint('userpanel', __name__)


@userpanel.route('/userpanel/login', methods=['GET', 'POST'])
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


@userpanel.route('/userpanel/logout')
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('userpanel.login_view'))


@userpanel.route('/userpanel/register', methods=['GET', 'POST'])
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


@userpanel.route('/userpanel/', methods=['GET'], strict_slashes=False)
@login_required
def userpanel_view():
    return redirect(url_for('userpanel.dashboard_view'))


@userpanel.route('/userpanel/dashboard', methods=['GET'])
@login_required
def dashboard_view():
    activity = (
        CustomerActivity.query.with_entities(
            CustomerActivity.url, CustomerActivity.module_name, func.count(CustomerActivity.url).label('count')
        )
        .filter_by(customer=current_user)
        .group_by(CustomerActivity.url, CustomerActivity.module_name)
        .all()
    )

    statistics = {}
    statistics['total_calculations'] = CustomerCalculation.query.filter_by(customer=current_user).count()
    statistics['total_visits'] = CustomerActivity.query.filter_by(customer=current_user).count()
    return render_template(
        'userpanel/dashboard.html', title="Dashboard", user=current_user.login, activity=activity, statistics=statistics
    )


@userpanel.route('/userpanel/editprofile', methods=['GET', 'POST'])
@login_required
def edit_profile_view():
    profile = Customer.query.get_or_404(current_user.id)
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
            url_for('userpanel.calculations_search_view', query=query, order_by=order_by, sort_by=sort_by, page=page)
        )

    if sort_by == "desc":
        calculations = (
            CustomerCalculation.query.filter_by(customer=current_user)
            .order_by(desc(order_by))
            .paginate(page=page, per_page=per_page)
        )
    elif sort_by == "asc":
        calculations = (
            CustomerCalculation.query.filter_by(customer=current_user)
            .order_by(asc(order_by))
            .paginate(page=page, per_page=per_page)
        )
    else:
        calculations = (
            CustomerCalculation.query.filter_by(customer=current_user)
            .order_by(desc(order_by))
            .paginate(page=page, per_page=per_page)
        )

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
        calculations = (
            CustomerCalculation.query.filter(CustomerCalculation.title.like(f'%{query}%'))
            .filter(CustomerCalculation.customer == current_user)
            .order_by(desc(order_by))
            .paginate(page=page, per_page=per_page)
        )
    elif sort_by == "asc":
        calculations = (
            CustomerCalculation.query.filter(CustomerCalculation.title.like(f'%{query}%'))
            .filter(CustomerCalculation.customer == current_user)
            .order_by(asc(order_by))
            .paginate(page=page, per_page=per_page)
        )
    else:
        calculations = (
            CustomerCalculation.query.filter(CustomerCalculation.title.like(f'%{query}%'))
            .filter(CustomerCalculation.customer == current_user)
            .order_by(desc(order_by))
            .paginate(page=page, per_page=per_page)
        )

    return render_template('userpanel/calculations/calculations.html', calculations=calculations)


@userpanel.route('/userpanel/calculations/delete/<int:calculation_id>')
@login_required
def calculation_delete_view(calculation_id):
    calculation = CustomerCalculation.query.filter_by(id=calculation_id).first()
    db.session.delete(calculation)
    db.session.commit()

    flash('You have successfully deleted the calculation.', 'success')

    return redirect(url_for('userpanel.calculations_list_view'))


@userpanel.route('/userpanel/calculations/<int:calculation_id>')
@login_required
def calculation_details_view(calculation_id):
    calculation = CustomerCalculation.query.filter_by(id=calculation_id).first()

    return render_template('userpanel/calculations/calculation_details.html', calculation=calculation)


@userpanel.route('/userpanel/pages')
@login_required
@superuser_required
def pages_list_view():
    pages = Page.query.order_by(asc(Page.id)).all()
    return render_template('userpanel/pages/pages.html', pages=pages)


@userpanel.route('/userpanel/pages/<int:page_id>', methods=['GET', 'POST'])
@login_required
@superuser_required
def page_details_view(page_id):
    page = Page.query.get_or_404(page_id)
    form = PageEditForm(obj=page)

    if form.validate_on_submit():
        page.name = form.name.data
        page.is_active = form.is_active.data
        page.slug = form.slug.data
        page.seo_title = form.seo_title.data
        page.seo_desc = form.seo_desc.data
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
@superuser_required
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
@superuser_required
def page_delete_view(page_id):
    page = Page.query.get_or_404(page_id)

    db.session.delete(page)
    db.session.commit()

    flash('You have successfully delete the page - {}.'.format(page.name), 'success')

    return redirect(url_for('userpanel.pages_list_view'))


@userpanel.route('/userpanel/customers/')
@login_required
@superuser_required
def customers_list_view():
    customers = Customer.query.order_by(Customer.id).all()
    return render_template('userpanel/customers/customers.html', customers=customers)


@userpanel.route('/userpanel/customers/<int:customer_id>', methods=['GET', 'POST'])
@login_required
@superuser_required
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
@superuser_required
def customer_delete_view(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    db.session.delete(customer)
    db.session.commit()

    flash('You have successfully delete the customer - {}.'.format(customer.login), 'success')

    return redirect(url_for('userpanel.customers_list_view'))


@userpanel.route('/userpanel/models', methods=['GET'])
@login_required
def apmc_list_view():
    order_by = request.args.get('order_by', "created_at")
    sort_by = request.args.get('sort_by')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if sort_by == "desc":
        apmc_data_list = (
            APMCData.query.filter_by(customer=current_user, training_completed=True)
            .order_by(desc(order_by))
            .paginate(page=page, per_page=per_page)
        )
    elif sort_by == "asc":
        apmc_data_list = (
            APMCData.query.filter_by(customer=current_user, training_completed=True)
            .order_by(asc(order_by))
            .paginate(page=page, per_page=per_page)
        )
    else:
        apmc_data_list = (
            APMCData.query.filter_by(customer=current_user, training_completed=True)
            .order_by(desc(order_by))
            .paginate(page=page, per_page=per_page)
        )

    return render_template('userpanel/apmc/apmc_data_list.html', apmc_data_list=apmc_data_list)


@userpanel.route('/userpanel/models/<int:apmc_data_id>', methods=['GET', 'POST'])
@login_required
def apmc_details_view(apmc_data_id):
    apmc_data = APMCData.query.get_or_404(apmc_data_id)

    apmc_service = APMCUserPanelService(apmc_data)

    ModelForm.update_form(ModelForm, apmc_service.get_X_names())
    form = ModelForm(request.form)

    context = {'form': form, 'apmc_data': apmc_data, 'model_metric': apmc_service.get_model_metric()}

    if form.validate_on_submit():
        input_values = [value for key, value in form.data.items() if key != 'csrf_token']
        apmc_service.set_user_input(input_values)

        flash(f'You have successfully predicted.', 'success')
        slack_notification.apmc_made_prediction(current_user, apmc_data)

        return render_template(
            'userpanel/apmc/apmc_data_details.html',
            context=context,
            predicted_data=apmc_service.get_predicted_data(),
            extrapolation_risk_msg=apmc_service.get_extrapolation_risk(),
        )

    return render_template('userpanel/apmc/apmc_data_details.html', context=context)


@userpanel.route('/userpanel/models/delete/<int:apmc_data_id>')
@login_required
def apmc_delete_view(apmc_data_id):
    apmc_data = APMCData.query.get_or_404(apmc_data_id)

    db.session.delete(apmc_data)
    db.session.commit()
    remove_file(apmc_data.model_path())

    flash('You have successfully delete the model - {}.'.format(apmc_data.project_name), 'success')

    return redirect(url_for('userpanel.apmc_list_view'))


@userpanel.route('/userpanel/models/report/<int:apmc_data_id>')
@login_required
def apmc_report_view(apmc_data_id):
    apmc_data = APMCData.query.get_or_404(apmc_data_id)

    slack_notification.apmc_report_downloaded(current_user, apmc_data)

    if apmc_data.report:
        return send_from_directory(APMC_REPORTS_UPLOAD_PATH, apmc_data.report)
    else:
        report_generator = ReportGenerator(apmc_data)
        report_filename = report_generator.generate_report()

        apmc_data.report = report_filename

        db.session.add(apmc_data)
        db.session.commit()

        return send_from_directory(APMC_REPORTS_UPLOAD_PATH, apmc_data.report)


@userpanel.route('/userpanel/models/report/tree-graph/<int:apmc_data_id>')
@login_required
def apmc_report_tree_graph_view(apmc_data_id):
    apmc_data = APMCData.query.get_or_404(apmc_data_id)

    slack_notification.apmc_tree_graph_downloaded(current_user, apmc_data)

    report_generator = ReportGenerator(apmc_data)
    tree_graph = report_generator.get_tree_graph()

    response = make_response(tree_graph)
    response.headers['Content-Type'] = 'image/svg+xml'
    response.headers['Content-Disposition'] = 'inline; filename=report-tree-graph.svg'

    return response


@userpanel.route('/statistics/all-calculations')
@login_required
@superuser_required
def statistics_calculations_list_view():
    calculations = Calculation.query.order_by(Calculation.created_at).all()

    return render_template('userpanel/statistics/calculations.html', calculations=calculations)


@userpanel.route('/statistics/all-customers-calculations')
@login_required
@superuser_required
def statistics_customers_calculations_list_view():
    calculations = CustomerCalculation.query.order_by(CustomerCalculation.created_at).all()

    return render_template('userpanel/statistics/customers_calculations.html', calculations=calculations)


@userpanel.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
