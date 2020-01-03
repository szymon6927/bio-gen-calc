from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import login_required
from sqlalchemy import func

from app.apmc.models import APMCData
from app.customer_calculation.models import CustomerCalculation
from app.database import db
from app.userpanel.decorators import superuser_required
from app.userpanel.forms import AdminCustomerEditForm
from app.userpanel.models import Customer
from app.userpanel.models import CustomerActivity
from app.userpanel.views import userpanel


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

    activity = (
        CustomerActivity.query.with_entities(
            CustomerActivity.url, CustomerActivity.module_name, func.count(CustomerActivity.url).label('count')
        )
        .filter_by(customer=customer)
        .group_by(CustomerActivity.url, CustomerActivity.module_name)
        .all()
    )

    statistics = dict()
    statistics['total_calculations'] = CustomerCalculation.query.filter_by(customer=customer).count()
    statistics['total_visits'] = CustomerActivity.query.filter_by(customer=customer).count()
    statistics['total_apmc'] = APMCData.query.filter_by(customer=customer).count()

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

    return render_template(
        'userpanel/customers/customer_details.html',
        form=form,
        customer=customer,
        activity=activity,
        statistics=statistics,
    )


@userpanel.route('/userpanel/customers/delete/<int:customer_id>')
@login_required
@superuser_required
def customer_delete_view(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    customer_activity = CustomerActivity.query.filter_by(customer_id=customer_id).first()

    if customer_activity:
        db.session.delete(customer_activity)

    db.session.delete(customer)
    db.session.commit()

    flash('You have successfully delete the customer - {}.'.format(customer.login), 'success')

    return redirect(url_for('userpanel.customers_list_view'))
