from flask import render_template
from . import privacy_policy


@privacy_policy.route('/privacy-policy', methods=['GET'])
def privacy_policy_page():
    """
    Render privacy policy page
    """
    return render_template('privacy_policy/index.html', title="Privacy Policy")
