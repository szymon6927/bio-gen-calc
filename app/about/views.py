from flask import render_template
from . import about


@about.route('/about')
def about_page():
    """
    Render the about template on the / route
    """
    return render_template('about/index.html', title="About Us")

