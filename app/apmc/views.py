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
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.apmc.config import APMC_DATASET_UPLOAD_PATH
from app.apmc.exceptions import DatasetValidationError
from app.apmc.models import APMCData
from app.apmc.services import pre_train
from app.apmc.services import train
from app.clients.slack_client import SlackNotification
from app.common.decorators import add_customer_activity
from app.database import db
from app.helpers.file_helper import allowed_file
from app.userpanel.models import Page

slack_notification = SlackNotification()
apmc = Blueprint('apmc', __name__)


@apmc.route('/apmc')
@add_customer_activity
def apmc_page():
    return render_template('apmc/index.html', title="APMC")


@apmc.route('/apmc/how-to-use')
@add_customer_activity
def apmc_how_to_use_page():
    return render_template('apmc/how_to_use.html', title="APMC - How to use")


@apmc.route('/apmc/documentation')
@add_customer_activity
def apmc_documentation_page():
    return render_template('apmc/documentation.html', title="APMC - Documentation")


@apmc.route('/apmc/pre-train', methods=['POST'])
@login_required
def apmc_pre_train():
    if 'file' not in request.files:
        abort(Response('No file part', 400))

    file = request.files['file']

    if file.filename == '':
        abort(Response('No selected file', 400))

    if file and allowed_file(file.filename):
        random_hex = secrets.token_hex(8)
        filename = f"{random_hex}_{secure_filename(file.filename)}"
        file.save(os.path.join(current_app.root_path, APMC_DATASET_UPLOAD_PATH, filename))

        apmc_data = APMCData(
            customer=current_user,
            project_name=request.form.get('project_name'),
            dataset=filename,
            model_type=request.form.get('model_type'),
            normalization=request.form.get('normalization') == "true",
            training_completed=False,
        )
        slack_notification.apmc_pre_train_calculation(
            current_user,
            request.form.get('project_name'),
            filename,
            request.form.get('model_type'),
            request.form.get('normalization'),
            request.remote_addr,
        )

        db.session.add(apmc_data)
        db.session.commit()

        try:
            result = pre_train(apmc_data)
            result.update({'data_id': apmc_data.id})
            return jsonify(result)
        except DatasetValidationError as e:
            abort(Response(str(e), 400))

    abort(Response('No file, or wrong file extension', 400))


@apmc.route('/apmc/train', methods=['POST'])
@login_required
def apmc_train():
    data = request.get_json()

    apmc_data_id = data.get('data_id')
    user_choice = data.get('selected_model')

    slack_notification.apmc_train_calculation(current_user, data, request.remote_addr)

    model_name = train(int(apmc_data_id), user_choice)

    return jsonify([data, model_name])


@apmc.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
