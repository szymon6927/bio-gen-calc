import base64
from flask import render_template, request, jsonify, abort, Response, make_response
from werkzeug.utils import secure_filename
from . import sequences_analysis_tools

from .utils.SequencesTools import SequencesTools
from .utils.ConsensusSequence import ConsensusSequence
from .utils.DotPlot import DotPlot

from ..helpers.file_helper import allowed_file


@sequences_analysis_tools.route('/sequences-analysis-tools/dot-plot')
def dot_plot_page():
    return render_template('sequences_analysis_tools/dot_plot.html', title="Dot plot")


@sequences_analysis_tools.route('/sequences-analysis-tools/dot-plot/send-raw-seq', methods=['POST'])
def dot_plot_raw_seq():
    try:
        data = request.get_json()
        dot_plot = DotPlot(data)
        result = dot_plot.raw_sequence()
        return jsonify({'data': result,
                        'dotplot_base64': dot_plot.get_dot_plot_image(),
                        'alignment': dot_plot.get_alignments()})
    except Exception as e:
        abort(Response(str(e), 400))


@sequences_analysis_tools.route('/sequences-analysis-tools/dot-plot/send-genebank-ids', methods=['POST'])
def dot_plot_genebank_ids():
    try:
        data = request.get_json()
        dot_plot = DotPlot(data)
        result = dot_plot.genebank_seq()
        return jsonify({'data': result,
                        'dotplot_base64': dot_plot.get_dot_plot_image(),
                        'alignment': dot_plot.get_alignments()})
    except Exception as e:
        abort(Response(str(e), 400))


@sequences_analysis_tools.route('/sequences-analysis-tools/consensus-sequence')
def consensus_sequence_page():
    return render_template('sequences_analysis_tools/consensus_sequence.html', title="Consensus Sequence")


@sequences_analysis_tools.route('/sequences-analysis-tools/consensus-sequence/send-raw-seq', methods=['POST'])
def get_raw_seq_data():
    try:
        data = request.get_json()
        consensus_seq = ConsensusSequence(data)
        result = consensus_seq.raw_sequence()
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
        filename = secure_filename(file.filename)

        data = dict()
        data['sequences'] = file.read()

        consensus_seq = ConsensusSequence(data)
        result = consensus_seq.file_seq()

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

        response = make_response(base64.b64encode(result.encode()))
        response.headers['Content-Type'] = 'text/plain'
        response.mimetype = 'text/plain'
        return response, 200
    except Exception as e:
        abort(Response(str(e), 400))


@sequences_analysis_tools.route('/sequences-analysis-tools/sequences-tools')
def sequences_tools_page():
    return render_template('sequences_analysis_tools/sequences_tools.html', title="Sequences Tools")


@sequences_analysis_tools.route('/sequences-analysis-tools/sequences-tools/send-data', methods=['POST'])
def get_sequences_data():
    try:
        data = request.get_json()
        seq_tools = SequencesTools(data)
        result = seq_tools.calculate()
        return jsonify({'data': result})
    except Exception as e:
        abort(Response(str(e), 400))
