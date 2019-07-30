from flask import render_template
from flask import request

from app.common.decorators import add_customer_activity
from app.donors import donors
from app.userpanel.models import Page


@donors.route('/donors')
@add_customer_activity
def donors_page():
    return render_template('donors/index.html', title="Our donors and cooperator")


@donors.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
