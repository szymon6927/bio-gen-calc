# app/home/__init__.py

from flask import Blueprint

about = Blueprint('about', __name__)

from . import views
