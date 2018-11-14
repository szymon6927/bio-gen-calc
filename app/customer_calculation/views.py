import json
from flask import request, jsonify, abort, Response
from . import customer_calculation
from ..database import db
from ..models.Userpanel import CustomerCalculation


@customer_calculation.route('/send-calculation', methods=['POST'])
def save_calculation():
    try:
        data = request.get_json()

        title = data.get('title')
        customer_id = data.get('customer_id')
        module_name = data.get('module_name')
        customer_input = data.get('customer_input')
        result = data.get('result').get('data')

        calculation = CustomerCalculation(customer_id=customer_id, title=title, module_name=module_name,
                                          customer_input=customer_input, result=json.dumps(result))
        db.session.add(calculation)
        db.session.commit()

        return jsonify({'info': "Calculation saved! Now you can see your calculation in user panel"})
    except Exception as e:
        abort(Response(str(e), 400))
