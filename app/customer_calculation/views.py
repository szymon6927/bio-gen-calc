import json
from flask import request, jsonify, abort, Response

from app.customer_calculation import customer_calculation
from app.customer_calculation.models import CustomerCalculation
from app.database import db
from app.userpanel.models import Customer


@customer_calculation.route('/send-calculation', methods=['POST'])
def save_calculation():
    try:
        data = request.get_json()

        title = data.get('title')
        customer_id = data.get('customer_id')
        module_name = data.get('module_name')
        customer_input = data.get('customer_input')
        result = data.get('result')

        customer = Customer.query.filter_by(id=customer_id).first()
        calculation = CustomerCalculation(customer=customer, title=title, module_name=module_name,
                                          customer_input=customer_input, result=json.dumps(result))
        db.session.add(calculation)
        db.session.commit()

        return jsonify({'info': "Calculation saved! Now you can see your calculation in user panel"})
    except Exception as e:
        abort(Response(str(e), 400))
