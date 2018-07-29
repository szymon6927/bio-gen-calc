from flask import render_template, request, jsonify
from . import hardy_weinber
from .utils import HardyWeinberCalculation


@hardy_weinber.route('/hardy-weinber-page')
def hardy_weinber_page():
    """
    Render the hardy_weinber template on the / route
    """
    return render_template('hardy_weinber/index.html', title="Hardy-Weinberg equilibrium")


@hardy_weinber.route('/hardy-weinber/send-data', methods=['POST'])
def get_data():
    data = request.get_json()
    hw = HardyWeinberCalculation(data)

    result = hw.calcualte()

    return jsonify({'data': result})
