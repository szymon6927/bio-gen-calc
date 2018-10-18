import json
from ..database import db
from ..models.Calculation import Calculation

def add_calculation(module_name=None, user_data=None, result=None, ip_address=None):
    # print(f'add_calculation parameters {module_name}, {user_data}, {result}, {ip_address}', flush=True)
    if module_name and user_data and result and ip_address:
        db_user_data = json.dumps(user_data)
        db_results = json.dumps(result)

        print(db_results, flush=True)

        calculation = Calculation(module_name=module_name, user_date=db_user_data, results=db_results, ip_address=ip_address)
        db.session.add(calculation)
        db.session.commit()
    else:
        raise ValueError("One of the parameters is not set (equal to None)")