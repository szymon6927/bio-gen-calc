import json
import numpy as np
from functools import wraps

from flask import request
from flask_login import current_user

from ..database import db
from ..models.Calculation import Calculation
from ..models.Userpanel import CustomerActivity


def add_calculation(module_name=None, user_data=None, result=None, ip_address=None):
    if module_name and user_data and result and ip_address:
        if type(result) is np.ndarray:
            result = result.tolist()

        calculation = Calculation(module_name=module_name, user_data=json.dumps(user_data), result=json.dumps(result),
                                  ip_address=ip_address)
        db.session.add(calculation)
        db.session.commit()
    else:
        raise ValueError("One of the parameters is not set (equal to None)")


def add_customer_activity(view):
    @wraps(view)
    def add_activity(*args, **kwargs):
        if current_user.is_authenticated:
            url = request.path
            url_to_module_name = {
                '/': "Homepage",
                '/materials-and-methods': "Materials & Methods",
                '/hardy-weinber-page': "Hardy-Weinberg equilibrium",
                '/chi-square-page': "Chi-Square tests",
                '/pic': "Polymorphic information content & Heterozygosity",
                '/genetic-distance': "Genetic Distance",
                '/sequences-analysis-tools/dot-plot': "Dot plot",
                '/sequences-analysis-tools/consensus-sequence': "Consensus Sequence",
                '/sequences-analysis-tools/sequences-tools': "Sequences Tools",
                '/about': "About",
                '/donors': "Our donors and cooperators",
                '/contact': "Contact Us",
                '/privacy-policy': "Privacy Policy"
            }

            module_name = url_to_module_name.get(url, url)
            activity = CustomerActivity(customer=current_user, module_name=module_name, url=url)

            db.session.add(activity)
            db.session.commit()
        return view(*args, **kwargs)
    return add_activity
