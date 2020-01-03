from flask import render_template
from flask_login import login_required

from app.apmc.models import APMCData
from app.customer_calculation.models import CustomerCalculation
from app.userpanel.decorators import superuser_required
from app.userpanel.models import Calculation
from app.userpanel.views import userpanel


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


@userpanel.route('/statistics/all-models')
@login_required
@superuser_required
def statistics_models_list_view():
    apmc_data = APMCData.query.order_by(APMCData.created_at).all()

    return render_template('userpanel/statistics/apmc_data_list.html', models=apmc_data)
