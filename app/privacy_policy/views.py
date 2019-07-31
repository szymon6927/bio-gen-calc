from flask import Blueprint
from flask import render_template
from flask import request

from app.common.decorators import add_customer_activity
from app.userpanel.models import Page

privacy_policy = Blueprint('privacy_policy', __name__)


@privacy_policy.route('/privacy-policy', methods=['GET'])
@add_customer_activity
def privacy_policy_page():
    return render_template('privacy_policy/index.html', title="Privacy Policy")


@privacy_policy.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
