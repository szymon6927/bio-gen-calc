from functools import wraps

from flask import request
from flask_login import current_user

from app.database import db
from app.userpanel.models import CustomerActivity
from app.userpanel.models import Page


def add_customer_activity(view):
    @wraps(view)
    def add_activity(*args, **kwargs):
        if current_user.is_authenticated:
            module_name = Page.query.filter_by(slug=request.path).first()

            if not module_name:
                raise ValueError(f"Can not find name for: {request.path}")

            activity = CustomerActivity(customer=current_user, module_name=module_name, url=request.path)

            db.session.add(activity)
            db.session.commit()
        return view(*args, **kwargs)

    return add_activity
