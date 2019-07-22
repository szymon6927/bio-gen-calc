from flask import render_template

from app.home import home
from app.userpanel.models import Page
from app.helpers.db_helper import add_customer_activity


@home.route('/')
@add_customer_activity
def homepage():
    pages = Page.query.filter_by(is_active=True)
    return render_template('home/index.html', title="Home", pages=pages)

