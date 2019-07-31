from flask import Blueprint
from flask import render_template
from flask import request

from app.common.decorators import add_customer_activity
from app.userpanel.models import Page

about = Blueprint('about', __name__)


@about.route('/about')
@add_customer_activity
def about_page():
    return render_template('about/index.html', title="About Us")


@about.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
