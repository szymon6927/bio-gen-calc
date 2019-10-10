from flask import Blueprint
from flask import Response
from flask import abort
from flask import jsonify
from flask import render_template
from flask import request

from app.common.constants import ModuleName
from app.common.decorators import add_customer_activity
from app.hardy_weinberg.ds.HardyWeinbergCalculation import HardyWeinbergCalculation
from app.hardy_weinberg.entities.hw_entity import HWEntity
from app.helpers.db_helper import add_calculation
from app.userpanel.models import Page

hardy_weinberg = Blueprint('hardy_weinberg', __name__)


@hardy_weinberg.route('/hardy-weinberg-page')
@add_customer_activity
def hardy_weinberg_page():
    return render_template('hardy_weinberg/index.html', title="Hardy-Weinberg equilibrium")


@hardy_weinberg.route('/hardy-weinberg/send-data', methods=['POST'])
def get_data():
    try:
        data: dict = request.get_json()

        entity = HWEntity(data.get('he'), data.get('he'), data.get('rho'), data.get('alfa'))
        hw = HardyWeinbergCalculation(entity)

        result = hw.calculate()

        add_calculation(
            module_name=ModuleName.HARDY_WEINBERG, user_data=data, result=result, ip_address=request.remote_addr
        )

        return jsonify({'data': result})
    except TypeError:
        abort(Response("Please check type of input data", 409))
    except Exception as e:
        abort(Response(str(e), 400))


@hardy_weinberg.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
