# app/chi_square/views.py

from flask import render_template, request, jsonify
from . import chi_square
from .utils import ChiSquareCalculation, ChiSquareGoodness


@chi_square.route('/chi-square-page')
def chi_square_page():
    """
    Render the chi_square_page template on the / route
    """
    return render_template('chi_square/index.html', title="Chi-Square tests")


@chi_square.route('/chi-square/send-data', methods=['POST'])
def get_data():
    data = request.get_json()

    chi = ChiSquareCalculation(data)
    result = chi.chi_square()

    return jsonify({'data': result})


@chi_square.route('/chi-square/send-data-goodness', methods=['POST'])
def get_goodness_data():
    data = request.get_json()

    chi_goodness = ChiSquareGoodness(data["observed"], data["expected"])
    result = chi_goodness.chi_square_goodness()

    return jsonify({'data': result})
