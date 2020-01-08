from flask import Blueprint
from flask import render_template
from flask import request

from app.common.decorators import add_customer_activity
from app.userpanel.models import Page

blog = Blueprint('blog', __name__)


@blog.route('/blog', methods=['GET'])
@add_customer_activity
def blog_page():
    return render_template('blog/index.html', title="Blog")


@blog.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}