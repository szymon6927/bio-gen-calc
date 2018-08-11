from flask import Blueprint

hardy_weinber = Blueprint('hardy_weinber', __name__)

from . import views
