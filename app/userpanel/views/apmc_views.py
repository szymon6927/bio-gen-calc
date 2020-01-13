from flask import flash
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from sqlalchemy import asc
from sqlalchemy import desc

from app.apmc.config import APMC_DATASET_UPLOAD_PATH
from app.apmc.config import APMC_REPORTS_UPLOAD_PATH
from app.apmc.ds.report.report_generator import ReportGenerator
from app.apmc.models import APMCData
from app.clients.slack_client import SlackNotification
from app.database import db
from app.helpers.file_helper import remove_file
from app.userpanel.forms import ModelForm
from app.userpanel.services.apmc_service import APMCUserPanelService
from app.userpanel.views import userpanel

slack_notification = SlackNotification()


@userpanel.route('/models', methods=['GET'])
@login_required
def apmc_list_view():
    order_by = request.args.get('order_by', "created_at")
    sort_by = request.args.get('sort_by')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if sort_by == "desc":
        apmc_data_list = (
            APMCData.query.filter_by(customer=current_user, training_completed=True)
            .order_by(desc(order_by))
            .paginate(page=page, per_page=per_page)
        )
    elif sort_by == "asc":
        apmc_data_list = (
            APMCData.query.filter_by(customer=current_user, training_completed=True)
            .order_by(asc(order_by))
            .paginate(page=page, per_page=per_page)
        )
    else:
        apmc_data_list = (
            APMCData.query.filter_by(customer=current_user, training_completed=True)
            .order_by(desc(order_by))
            .paginate(page=page, per_page=per_page)
        )

    return render_template('userpanel/apmc/apmc_data_list.html', apmc_data_list=apmc_data_list)


@userpanel.route('/models/<int:apmc_data_id>', methods=['GET', 'POST'])
@login_required
def apmc_details_view(apmc_data_id):
    apmc_data = APMCData.query.get_or_404(apmc_data_id)

    apmc_service = APMCUserPanelService(apmc_data)

    ModelForm.update_form(ModelForm, apmc_service.get_X_names())
    form = ModelForm(request.form)

    context = {'form': form, 'apmc_data': apmc_data, 'model_metric': apmc_service.get_model_metric()}

    if form.validate_on_submit():
        input_values = [value for key, value in form.data.items() if key != 'csrf_token']
        apmc_service.set_user_input(input_values)

        flash(f'You have successfully predicted.', 'success')
        slack_notification.apmc_made_prediction(current_user, apmc_data)

        return render_template(
            'userpanel/apmc/apmc_data_details.html',
            context=context,
            predicted_data=apmc_service.get_predicted_data(),
            extrapolation_risk_msg=apmc_service.get_extrapolation_risk(),
        )

    return render_template('userpanel/apmc/apmc_data_details.html', context=context)


@userpanel.route('/models/delete/<int:apmc_data_id>')
@login_required
def apmc_delete_view(apmc_data_id):
    apmc_data = APMCData.query.get_or_404(apmc_data_id)

    db.session.delete(apmc_data)
    db.session.commit()
    remove_file(apmc_data.model_path())

    flash('You have successfully delete the model - {}.'.format(apmc_data.project_name), 'success')

    if 'all-models' in request.headers.get('Referer'):
        return redirect(url_for('userpanel.statistics_models_list_view'))

    return redirect(url_for('userpanel.apmc_list_view'))


@userpanel.route('/models/report/<int:apmc_data_id>')
@login_required
def apmc_report_view(apmc_data_id):
    apmc_data = APMCData.query.get_or_404(apmc_data_id)

    slack_notification.apmc_report_downloaded(current_user, apmc_data)

    if apmc_data.report:
        return send_from_directory(APMC_REPORTS_UPLOAD_PATH, apmc_data.report)
    else:
        report_generator = ReportGenerator(apmc_data)
        report_filename = report_generator.generate_report()

        apmc_data.report = report_filename

        db.session.add(apmc_data)
        db.session.commit()

        return send_from_directory(APMC_REPORTS_UPLOAD_PATH, apmc_data.report)


@userpanel.route('/models/download-dataset/<int:apmc_data_id>')
@login_required
def apmc_download_dataset_view(apmc_data_id):
    apmc_data = APMCData.query.get_or_404(apmc_data_id)

    return send_from_directory(APMC_DATASET_UPLOAD_PATH, apmc_data.dataset)


@userpanel.route('/models/report/tree-graph/<int:apmc_data_id>')
@login_required
def apmc_report_tree_graph_view(apmc_data_id):
    apmc_data = APMCData.query.get_or_404(apmc_data_id)

    slack_notification.apmc_tree_graph_downloaded(current_user, apmc_data)

    report_generator = ReportGenerator(apmc_data)
    tree_graph = report_generator.get_tree_graph()

    response = make_response(tree_graph)
    response.headers['Content-Type'] = 'image/svg+xml'
    response.headers['Content-Disposition'] = 'inline; filename=report-tree-graph.svg'

    return response
