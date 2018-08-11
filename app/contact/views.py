from flask import render_template
from . import contact


@contact.route('/contact')
def contact_page():
    return render_template('contact/index.html', title="Contact Us")
