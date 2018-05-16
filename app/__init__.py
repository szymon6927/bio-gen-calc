# app/__init__.py

# third-party imports
from flask import Flask
from flask import Blueprint

# local imports
from config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .about import about as about_blueprint
    app.register_blueprint(about_blueprint)

    from .hardy_weinber import hardy_weinber as hardy_weinber
    app.register_blueprint(hardy_weinber)

    from .chi_square import chi_square as chi_square
    app.register_blueprint(chi_square)

    return app
