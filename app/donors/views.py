from flask import render_template
from . import donors

from ..helpers.db_helper import add_customer_activity


@donors.route('/donors')
@add_customer_activity
def donors_page():
    return render_template('donors/index.html', title="Our donors and cooperator")
