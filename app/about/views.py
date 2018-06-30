# app/home/views.py

from flask import render_template
from . import about
from .. import detect_domain


@about.route('/about')
def about_page():
    """
    Render the about template on the / route
    """
    detect_domain()
    return render_template('about/index.html', title="Materials & methods")

