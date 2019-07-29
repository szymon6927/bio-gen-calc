from flask import render_template, request

from app.materials_and_methods import materials_and_methods
from app.userpanel.models import Page
from app.helpers.db_helper import add_customer_activity


@materials_and_methods.route('/materials-and-methods')
@add_customer_activity
def materials_and_methods_page():
    return render_template('materials_and_methods/index.html', title="Materials & methods")


@materials_and_methods.context_processor
def inject():
    return {
        'module_desc': Page.query.filter_by(slug=request.path).first()
    }
