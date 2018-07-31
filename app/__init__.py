# app/__init__.py

from datetime import datetime
from flask import Flask, render_template
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from .admin.admin_config import create_admin_interface

# local imports
from config import app_config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    db.init_app(app)

    admin = create_admin_interface()
    admin.init_app(app)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .about import about as about_blueprint
    app.register_blueprint(about_blueprint)

    from .hardy_weinber import hardy_weinber as hardy_weinber
    app.register_blueprint(hardy_weinber)

    from .chi_square import chi_square as chi_square
    app.register_blueprint(chi_square)

    from .pic import pic as pic
    app.register_blueprint(pic)

    from .genetic_distance import genetic_distance as genetic_distance
    app.register_blueprint(genetic_distance)

    from .contact import contact as contact
    app.register_blueprint(contact)

    @app.errorhandler(404)
    def page_not_found(e):
        print(e)
        return render_template("404.html", title="404 Page not found!")

    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    return app
