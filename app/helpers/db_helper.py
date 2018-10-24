import json
from ..database import db
from ..models.Calculation import Calculation

def add_calculation(module_name=None, user_data=None, result=None, ip_address=None):
    if module_name and user_data and result and ip_address:
        calculation = Calculation(module_name=module_name, user_data=json.dumps(user_data), result=json.dumps(result), ip_address=ip_address)
        db.session.add(calculation)
        db.session.commit()
    else:
        raise ValueError("One of the parameters is not set (equal to None)")