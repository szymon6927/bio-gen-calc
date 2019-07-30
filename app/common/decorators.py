from datetime import datetime
from functools import update_wrapper
from functools import wraps

from flask import make_response
from flask import request
from flask_login import current_user

from app import db
from app.userpanel.models import CustomerActivity


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
                '/privacy-policy': "Privacy Policy",
            }

            module_name = url_to_module_name.get(url, url)
            activity = CustomerActivity(customer=current_user, module_name=module_name, url=url)

            db.session.add(activity)
            db.session.commit()
        return view(*args, **kwargs)

    return add_activity


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)
