from flask import Blueprint

materials_and_methods = Blueprint('materials_and_methods', __name__)

from . import views
