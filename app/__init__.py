# app/__init__.py

from datetime import datetime
import pdfkit
from flask import Flask, render_template, request, make_response, abort, Response
from .database import db
from .admin.models import User, Page

from flask_login import LoginManager
from flask_migrate import Migrate

# local imports
from config import app_config

from .admin.views import run_admin

login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    admin = run_admin()
    admin.init_app(app)

    db.init_app(app)
    migrate = Migrate(app, db)

    with app.test_request_context():
        db.create_all()

    register_blueprints(app)

    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

    @app.route('/generate-pdf', methods=['POST'])
    def generate_pdf():
        try:
            print(f'generate_pdf', flush=True)
            data = request.get_json()
            print(f'request_data: {data}', flush=True)

            template = render_template('utils/pdf_template.html', content=data['content'])
            pdf = pdfkit.from_string(template, False)

            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=example.pdf'
            response.mimetype = 'application/pdf'
            return response
        except Exception as e:
            print(f'Exception: {e}', flush=True)
            abort(Response(str(e)), 400)

    @app.errorhandler(404)
    def page_not_found(e):
        print(e)
        return render_template("404.html", title="404 Page not found!")

    @app.context_processor
    def inject_now():
        return {
            'now': datetime.utcnow(),
            'module_desc': Page.query.filter_by(breadcrumbs=request.path).first(),
        }

    return app


def register_blueprints(app):
    from .home import home as home_blueprint
    from .about import about as about_blueprint
    from .hardy_weinber import hardy_weinber as hardy_weinber
    from .chi_square import chi_square as chi_square
    from .pic import pic as pic
    from .genetic_distance import genetic_distance as genetic_distance
    from .contact import contact as contact

    app.register_blueprint(home_blueprint)
    app.register_blueprint(about_blueprint)
    app.register_blueprint(hardy_weinber)
    app.register_blueprint(chi_square)
    app.register_blueprint(pic)
    app.register_blueprint(genetic_distance)
    app.register_blueprint(contact)
