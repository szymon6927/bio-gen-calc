from flask import Response
from flask import abort
from flask import jsonify
from flask import render_template
from flask import request

from app.chi_square import chi_square
from app.chi_square.ds.ChiSquareCalculation import ChiSquareCalculation
from app.chi_square.ds.ChiSquareGoodness import ChiSquareGoodness
from app.helpers.constants import CHI_SQUARE
from app.helpers.constants import CHI_SQUARE_GOODNESS
from app.helpers.db_helper import add_calculation
from app.helpers.db_helper import add_customer_activity
from app.userpanel.models import Page


@chi_square.route('/chi-square-page')
@add_customer_activity
def chi_square_page():
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


@chi_square.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
