from flask import render_template, request

from app.privacy_policy import privacy_policy
from app.userpanel.models import Page
from app.helpers.db_helper import add_customer_activity


@privacy_policy.route('/privacy-policy', methods=['GET'])
@add_customer_activity
def privacy_policy_page():
    return render_template('privacy_policy/index.html', title="Privacy Policy")


@privacy_policy.context_processor
def inject():
    return {
        'module_desc': Page.query.filter_by(slug=request.path).first()
    }
