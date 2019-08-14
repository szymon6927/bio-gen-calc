from datetime import datetime
from functools import update_wrapper
from functools import wraps

from flask import abort
from flask import make_response
from flask_login import current_user


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


def superuser_required(view):
    @wraps(view)
    def decorator(*args, **kwargs):
        if not current_user.is_superuser:
            abort(403)

        return view(*args, **kwargs)

    return update_wrapper(decorator, view)
