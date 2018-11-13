from flask import Blueprint

customer_calculation = Blueprint('customer_calculation', __name__)

from . import views