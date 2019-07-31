from flask import Blueprint

genetic_distance = Blueprint('genetic_distance', __name__)

from . import views
