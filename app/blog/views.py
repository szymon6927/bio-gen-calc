from flask import Blueprint
from flask import render_template
from flask import request
from sqlalchemy import desc

from app.blog.models import Article
from app.common.decorators import add_customer_activity
from app.userpanel.models import Page

blog = Blueprint('blog', __name__)


@blog.route('/blog', methods=['GET'])
@add_customer_activity
def blog_page():
    page = request.args.get('page', 1, type=int)
    articles = Article.query.order_by(desc('pub_date')).paginate(page=page, per_page=8)
    return render_template('blog/index.html', title="Blog", articles=articles)


@blog.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
