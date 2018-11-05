from flask import Blueprint

userpanel = Blueprint('userpanel', __name__)

from . import views
