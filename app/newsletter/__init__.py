from flask import Blueprint

newsletter = Blueprint('newsletter', __name__)

from . import views
