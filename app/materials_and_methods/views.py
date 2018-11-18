from flask import render_template
from . import materials_and_methods

from ..helpers.db_helper import add_customer_activity


@materials_and_methods.route('/materials-and-methods')
@add_customer_activity
def materials_and_methods_page():
    """
    Render the about template on the / route
    """
    return render_template('materials_and_methods/index.html', title="Materials & methods")

