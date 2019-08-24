import os
import secrets

from flask import Blueprint
from flask import Response
from flask import abort
from flask import current_app
from flask import jsonify
from flask import render_template
from flask import request
from flask_login import current_user
from werkzeug.utils import secure_filename

from app.ampc.config import AMPC_UPLOAD_PATH
from app.ampc.models import AMPCData
from app.common.decorators import add_customer_activity
from app.database import db
from app.helpers.file_helper import allowed_file
from app.userpanel.models import Page

ampc = Blueprint('ampc', __name__)


@ampc.route('/ampc')
@add_customer_activity
def ampc_page():
    return render_template('ampc/index.html', title="AMPC")


@ampc.route('/ampc/pre-train', methods=['POST'])
def ampc_pre_train():
    if 'file' not in request.files:
        abort(Response('No file part', 400))

    file = request.files['file']

    if file.filename == '':
        abort(Response('No selected file', 400))

    if file and allowed_file(file.filename):
        random_hex = secrets.token_hex(8)
        filename = f"{random_hex}_{secure_filename(file.filename)}"
        file.save(os.path.join(current_app.root_path, AMPC_UPLOAD_PATH, filename))

        ampc_data = AMPCData(
            customer=current_user,
            project_name=request.form.get('project_name'),
            dataset=filename,
            model_type=request.form.get('model_type'),
            normalization=request.form.get('normalization') == "true",
        )

        db.session.add(ampc_data)
        db.session.commit()

        return jsonify(
            {
                'project_name': request.form.get('project_name'),
                'dataset': filename,
                'model_type': request.form.get('model_type'),
                'normalization': request.form.get('normalization'),
            }
        )

    abort(Response('No file, or wrong file extension', 400))


@ampc.route('/ampc/train', methods=['POST'])
def ampc_train():
    pass


@ampc.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
