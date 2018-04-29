# app/home/views.py

from flask import render_template
from . import about


@about.route('/')
def about():
    """
    Render the about template on the / route
    """
    return render_template('about/index.html', title="About")

