from flask import render_template
from . import privacy_policy

from ..helpers.db_helper import add_customer_activity


@privacy_policy.route('/privacy-policy', methods=['GET'])
@add_customer_activity
def privacy_policy_page():
    """
    Render privacy policy page
    """
    return render_template('privacy_policy/index.html', title="Privacy Policy")
