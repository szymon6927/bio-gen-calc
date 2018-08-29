from flask import render_template, request, jsonify, abort, Response
from . import sequences_analysis_tools

from .utils.SequencesTools import SequencesTools
from .utils.ConsensusSequence import ConsensusSequence


@sequences_analysis_tools.route('/sequences-analysis-tools/dot-plot')
def dot_plot_page():
    return render_template('sequences_analysis_tools/dot_plot.html', title="Dot plot")


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
