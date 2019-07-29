from flask import render_template, request, jsonify, abort, Response

from app.hardy_weinber import hardy_weinber
from app.hardy_weinber.utils.HardyWeinberCalculation import HardyWeinberCalculation

from app.userpanel.models import Page

from app.helpers.db_helper import add_calculation
from app.helpers.db_helper import add_customer_activity
from app.helpers.constants import HARDY_WEINBERG


@hardy_weinber.route('/hardy-weinber-page')
@add_customer_activity
def hardy_weinber_page():
    """
    Render the hardy_weinber template on the / route
    """
    return render_template('hardy_weinber/index.html', title="Hardy-Weinberg equilibrium")


@hardy_weinber.route('/hardy-weinber/send-data', methods=['POST'])
def get_data():
    try:
        data = request.get_json()
        hw = HardyWeinberCalculation(data)

        result = hw.calcualte()

        add_calculation(module_name=HARDY_WEINBERG, user_data=data, result=result, ip_address=request.remote_addr)

        return jsonify({'data': result})
    except TypeError:
        abort(Response("Please check type of input data", 409))
    except Exception as e:
        abort(Response(str(e), 400))


@hardy_weinber.context_processor
def inject():
    return {
        'module_desc': Page.query.filter_by(slug=request.path).first()
    }
