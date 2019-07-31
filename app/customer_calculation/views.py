import json

from flask import Blueprint
from flask import Response
from flask import abort
from flask import jsonify
from flask import request
from flask_login import current_user

from app.customer_calculation.models import CustomerCalculation
from app.database import db

customer_calculation = Blueprint('customer_calculation', __name__)


@customer_calculation.route('/send-calculation', methods=['POST'])
def save_calculation():
    try:
        data = request.get_json()

        title = data.get('title')
        module_name = data.get('module_name')
        customer_input = data.get('customer_input')
        result = data.get('result')

        calculation = CustomerCalculation(
            customer=current_user,
            title=title,
            module_name=module_name,
            customer_input=customer_input,
            result=json.dumps(result),
        )
        db.session.add(calculation)
        db.session.commit()

        return jsonify({'info': "Calculation saved! Now you can see your calculation in user panel"})
    except Exception as e:
        abort(Response(str(e), 400))
