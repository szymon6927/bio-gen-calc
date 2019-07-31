import base64

from flask import Response
from flask import abort
from flask import jsonify
from flask import make_response
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename

from app.common.constants import ModuleName
from app.common.decorators import add_customer_activity
from app.helpers.db_helper import add_calculation
from app.helpers.file_helper import allowed_file
from app.sequences_analysis_tools import sequences_analysis_tools
from app.sequences_analysis_tools.ds.ConsensusSequence import ConsensusSequence
from app.sequences_analysis_tools.ds.DotPlot import DotPlot
from app.sequences_analysis_tools.ds.SequencesTools import SequencesTools
from app.userpanel.models import Page


@sequences_analysis_tools.route('/sequences-analysis-tools/dot-plot')
@add_customer_activity
def dot_plot_page():
    return render_template('sequences_analysis_tools/dot_plot.html', title="Dot plot")


@sequences_analysis_tools.route('/sequences-analysis-tools/dot-plot/send-raw-seq', methods=['POST'])
def dot_plot_raw_seq():
    try:
        data = request.get_json()
        dot_plot = DotPlot(data)
        result = dot_plot.raw_sequence()

        add_calculation(
            module_name=ModuleName.DOT_PLOT_RAW_SEQ, user_data=data, result=result, ip_address=request.remote_addr
        )

        return jsonify(
            {'data': result, 'dotplot_base64': dot_plot.get_dot_plot_image(), 'alignment': dot_plot.get_alignments()}
        )
    except Exception as e:
        abort(Response(str(e), 400))


@sequences_analysis_tools.route('/sequences-analysis-tools/dot-plot/send-genebank-ids', methods=['POST'])
def dot_plot_genebank_ids():
    try:
        data = request.get_json()
        dot_plot = DotPlot(data)
        result = dot_plot.genebank_seq()

        add_calculation(
            module_name=ModuleName.DOT_PLOT_GENEBANK_IDS, user_data=data, result=result, ip_address=request.remote_addr
        )

        return jsonify(
            {'data': result, 'dotplot_base64': dot_plot.get_dot_plot_image(), 'alignment': dot_plot.get_alignments()}
        )
    except Exception as e:
        abort(Response(str(e), 400))


@sequences_analysis_tools.route('/sequences-analysis-tools/consensus-sequence')
@add_customer_activity
def consensus_sequence_page():
    return render_template('sequences_analysis_tools/consensus_sequence.html', title="Consensus Sequence")


@sequences_analysis_tools.route('/sequences-analysis-tools/consensus-sequence/send-raw-seq', methods=['POST'])
def get_raw_seq_data():
    try:
        data = request.get_json()
        consensus_seq = ConsensusSequence(data)
        result = consensus_seq.raw_sequence()

        add_calculation(
            module_name=ModuleName.CONSENSUS_SEQUENCE_RAW_SEQ,
            user_data=data,
            result=result,
            ip_address=request.remote_addr,
        )

        return jsonify({'data': result})
    except Exception as e:
        abort(Response(str(e), 400))


@sequences_analysis_tools.route('/sequences-analysis-tools/consensus-sequence/send-seq-file', methods=['POST'])
def get_seq_file_data():
    if 'file' not in request.files:
        abort(Response('No file part', 400))

    file = request.files['file']

    if file.filename == '':
        abort(Response('No selected file', 400))

    if file and allowed_file(file.filename):
        secure_filename(file.filename)  # TODO: secure_filename return correct filename, we should do sth with this

        data = dict()
        data['sequences'] = file.read().decode()
        data['threshold'] = request.form['threshold']

        consensus_seq = ConsensusSequence(data)
        result = consensus_seq.file_seq()

        add_calculation(
            module_name=ModuleName.CONSENSUS_SEQUENCE_FILE_SEQ,
            user_data=data,
            result=result,
            ip_address=request.remote_addr,
        )

        response = make_response(base64.b64encode(result.encode()))
        response.headers['Content-Type'] = 'text/plain'
        response.mimetype = 'text/plain'
        return response, 200
    else:
        abort(Response('Illegal file extension', 400))


@sequences_analysis_tools.route('/sequences-analysis-tools/consensus-sequence/send-genebank-file', methods=['POST'])
def get_seq_genebank():
    try:
        data = request.get_json()
        consensus_seq = ConsensusSequence(data)
        result = consensus_seq.genebank_seq()

        add_calculation(
            module_name=ModuleName.CONSENSUS_SEQUENCE_GENE_BANK,
            user_data=data,
            result=result,
            ip_address=request.remote_addr,
        )

        response = make_response(base64.b64encode(result.encode()))
        response.headers['Content-Type'] = 'text/plain'
        response.mimetype = 'text/plain'
        return response, 200
    except Exception as e:
        abort(Response(str(e), 400))


@sequences_analysis_tools.route('/sequences-analysis-tools/sequences-tools')
@add_customer_activity
def sequences_tools_page():
    return render_template('sequences_analysis_tools/sequences_tools.html', title="Sequences Tools")


@sequences_analysis_tools.route('/sequences-analysis-tools/sequences-tools/send-data', methods=['POST'])
def get_sequences_data():
    try:
        data = request.get_json()
        seq_tools = SequencesTools(data)
        result = seq_tools.calculate()

        add_calculation(
            module_name=ModuleName.SEQUENCES_TOOLS, user_data=data, result=result, ip_address=request.remote_addr
        )

        return jsonify({'data': result})
    except Exception as e:
        abort(Response(str(e), 400))


@sequences_analysis_tools.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
