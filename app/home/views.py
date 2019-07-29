from flask import render_template
from flask import request

from app.home import home
from app.userpanel.models import Page
from app.helpers.db_helper import add_customer_activity


@home.route('/')
@add_customer_activity
def homepage():
    pages = Page.query.filter_by(is_active=True)
    return render_template('home/index.html', title="Home", pages=pages)


@home.context_processor
def inject():
    return {
        'module_desc': Page.query.filter_by(slug=request.path).first()
    }
