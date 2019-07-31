from flask import Blueprint
from flask import render_template
from flask import request

from app.common.decorators import add_customer_activity
from app.userpanel.models import Page

materials_and_methods = Blueprint('materials_and_methods', __name__)


@materials_and_methods.route('/materials-and-methods')
@add_customer_activity
def materials_and_methods_page():
    return render_template('materials_and_methods/index.html', title="Materials & methods")


@materials_and_methods.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
