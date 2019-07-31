from flask import Blueprint
from flask import render_template
from flask import request

from app.common.decorators import add_customer_activity
from app.userpanel.models import Page

home = Blueprint('home', __name__)


@home.route('/')
@add_customer_activity
def homepage():
    pages = Page.query.filter_by(is_active=True)
    return render_template('home/index.html', title="Home", pages=pages)


@home.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
