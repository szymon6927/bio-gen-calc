from flask import render_template
from . import about
from ..helpers.db_helper import add_customer_activity


@about.route('/about')
@add_customer_activity
def about_page():
    """
    Render the about template on the / route
    """
    return render_template('about/index.html', title="About Us")

