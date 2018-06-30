# app/chi_square/views.py

from flask import render_template
from . import contact
from .. import detect_domain


@contact.route('/contact')
def contact_page():
    """
    Render the chi_square_page template on the / route
    """
    detect_domain()
    return render_template('contact/index.html', title="Contact Us")
