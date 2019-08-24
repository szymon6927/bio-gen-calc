from flask import Blueprint
from flask import Response
from flask import abort
from flask import render_template
from flask import request

from app.common.decorators import add_customer_activity
from app.helpers.file_helper import allowed_file
from app.userpanel.models import Page

ampc = Blueprint('ampc', __name__)


@ampc.route('/ampc')
@add_customer_activity
def ampc_page():
    return render_template('ampc/index.html', title="AMPC")


@ampc.route('/ampc/calculate')
def calculate_ampc():
    if 'file' not in request.files:
        abort(Response('No file part', 400))

    file = request.files['file']

    if file.filename == '':
        abort(Response('No selected file', 400))

    if file and allowed_file(file.filename):

        data = dict()
        data['sequences'] = file.read().decode()


@ampc.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
