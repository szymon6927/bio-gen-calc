from flask import render_template, request, jsonify, abort, Response
from . import chi_square
from .utils.ChiSquareCalculation import ChiSquareCalculation
from .utils.ChiSquareGoodness import ChiSquareGoodness

from ..helpers.db_helper import add_calculation, add_customer_activity
from ..helpers.constants import CHI_SQUARE, CHI_SQUARE_GOODNESS


@chi_square.route('/chi-square-page')
@add_customer_activity
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

        add_calculation(module_name=CHI_SQUARE, user_data=data, result=result, ip_address=request.remote_addr)

        return jsonify({'data': result})
    except TypeError as e:
        abort(Response(f'Please check type of input data, {str(e)}', 409))
    except Exception as e:
        abort(Response(str(e), 400))


@chi_square.route('/chi-square/send-data-goodness', methods=['POST'])
def get_goodness_data():
    try:
        data = request.get_json()

        chi_goodness = ChiSquareGoodness(data["observed"], data["expected"])
        result = chi_goodness.calculate()

        add_calculation(module_name=CHI_SQUARE_GOODNESS, user_data=data, result=result, ip_address=request.remote_addr)

        return jsonify({'data': result})
    except TypeError as e:
        abort(Response(f'Please check type of input data, {str(e)}', 409))
    except Exception as e:
        abort(Response(str(e), 400))
