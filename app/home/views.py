from flask import render_template
from . import home
from ..admin.models import Page


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    pages = Page.query.filter_by(is_active=True)
    return render_template('home/index.html', title="Home", pages=pages)

