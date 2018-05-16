# app/chi_squiare/__init__.py

from flask import Blueprint

chi_square = Blueprint('chi_square', __name__)

from . import views
