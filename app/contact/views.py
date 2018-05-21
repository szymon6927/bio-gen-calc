# app/chi_square/views.py

from flask import render_template
from . import contact


@contact.route('/contact')
def contact_page():
    """
    Render the chi_square_page template on the / route
    """
    return render_template('contact/index.html', title="Contact Us")