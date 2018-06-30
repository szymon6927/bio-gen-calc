# app/home/views.py

from flask import render_template
from . import home
from .. import detect_domain


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    detect_domain()
    return render_template('home/index.html', title="Home")

