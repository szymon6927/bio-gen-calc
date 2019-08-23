from flask import Blueprint
from flask import render_template
from flask import request

from app.common.decorators import add_customer_activity
from app.userpanel.models import Page

ampc = Blueprint('ampc', __name__)


@ampc.route('/ampc')
@add_customer_activity
def ampc_page():
    return render_template('ampc/index.html', title="AMPC")


@ampc.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
