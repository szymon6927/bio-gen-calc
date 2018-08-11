from flask import Blueprint

donors = Blueprint('donors', __name__)

from . import views
