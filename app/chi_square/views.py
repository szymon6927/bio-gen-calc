from flask import render_template, request, jsonify, abort, Response
from . import chi_square
from .utils.ChiSquareCalculation import ChiSquareCalculation
from .utils.ChiSquareGoodness import ChiSquareGoodness


@chi_square.route('/chi-square-page')
def chi_square_page():
    """
    Render the chi_square_page template on the / route
    """
    return render_template('chi_square/index.html', title="Chi-Square tests")


@chi_square.route('/chi-square/send-data', methods=['POST'])
def get_data():
    try:
        data = request.get_json()

        chi = ChiSquareCalculation(data)
        result = chi.calculate()

        return jsonify({'data': result})
    except TypeError:
        abort(Response("Please check type of input data", 409))
    except Exception as e:
        abort(Response(str(e), 400))


@chi_square.route('/chi-square/send-data-goodness', methods=['POST'])
def get_goodness_data():
    try:
        data = request.get_json()

        chi_goodness = ChiSquareGoodness(data["observed"], data["expected"])
        result = chi_goodness.calculate()

        return jsonify({'data': result})
    except TypeError:
        abort(Response("Please check type of input data", 409))
    except Exception as e:
        abort(Response(str(e), 400))
