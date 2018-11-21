from flask import render_template
from . import home
from ..models.Admin import Page
from ..helpers.db_helper import add_customer_activity


@home.route('/')
@add_customer_activity
def homepage():
    """
    Render the homepage template on the / route
    """
    pages = Page.query.filter_by(is_active=True)
    return render_template('home/index.html', title="Home", pages=pages)

