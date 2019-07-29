from flask import render_template, request

from app.donors import donors
from app.helpers.db_helper import add_customer_activity
from app.userpanel.models import Page


@donors.route('/donors')
@add_customer_activity
def donors_page():
    return render_template('donors/index.html', title="Our donors and cooperator")


@donors.context_processor
def inject():
    return {
        'module_desc': Page.query.filter_by(slug=request.path).first()
    }
