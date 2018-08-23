from flask import Blueprint

sequences_analysis_tools = Blueprint('sequences_analysis_tools', __name__)

from . import views
