from flask import Blueprint

privacy_policy = Blueprint('privacy_policy', __name__)

from . import views
