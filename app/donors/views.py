from flask import render_template
from . import donors


@donors.route('/donors')
def donors_page():
    return render_template('donors/index.html', title="Our donors and cooperator")
