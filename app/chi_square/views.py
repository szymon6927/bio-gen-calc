# app/chi_square/views.py

from flask import render_template, flash
from . import chi_square


@chi_square.route('/chi_square_page')
def chi_square_page():
    """
    Render the chi_square_page template on the / route
    """
    return render_template('chi_square/index.html', title="Chi Square equalibration")
