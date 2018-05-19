# app/chi_square/views.py

from flask import render_template, request, jsonify
from . import chi_square
from .utils import ChiSquareCalculation, ChiSquareGoodness


@chi_square.route('/chi_square_page')
def chi_square_page():
    """
    Render the chi_square_page template on the / route
    """
    return render_template('chi_square/index.html', title="Chi Square equalibration")


@chi_square.route('/sendData', methods=['POST'])
def get_data():
    data = request.get_json()

    chi = ChiSquareCalculation(data)
    data = chi.chi_square()

    return jsonify({'data': data})


@chi_square.route('/sendDataGoodness', methods=['POST'])
def get_goodness_data():
    data = request.get_json()

    chi_goodness = ChiSquareGoodness(data["observed"], data["expected"])
    result = chi_goodness.chi_square_goodness()

    return jsonify({'data': result})
