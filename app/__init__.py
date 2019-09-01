import base64
import os
from datetime import datetime

import pdfkit
from flask import Flask
from flask import Response
from flask import abort
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for
from flask_compress import Compress
from flask_htmlmin import HTMLMIN
from flask_login import LoginManager
from flask_migrate import Migrate

from app.database import db
from config import app_config

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

login_manager = LoginManager()
migrate = Migrate()
compress = Compress()
htmlmin = HTMLMIN()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)
    register_jinja_templte_filters(app)

    login_manager.init_app(app)
    login_manager.login_view = 'userpanel.login_view'

    compress.init_app(app)
    htmlmin.init_app(app)

    @app.route('/robots.txt')
    @app.route('/sitemap.xml')
    def serve_static_seo_files():
        return send_from_directory(app.static_folder, request.path[1:])

    @app.route('/generate-pdf', methods=['POST'])
    def generate_pdf():
        try:
            data = request.get_json()

            template = render_template('utils/pdf_template.html', content=data['content'])
            css = [
                'app/static/css/vendors/bootstrap.min.css',
                'app/static/css/style.css',
                'app/static/css/pdf-style.css',
            ]
            try:
                pdf = base64.b64encode(pdfkit.from_string(template, False, css=css))
            except FileNotFoundError:
                pdf = base64.b64encode(pdfkit.from_string(template, False))

            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.mimetype = 'application/pdf'
            return response, 200
        except Exception as e:
            abort(Response(str(e)), 400)

    @app.route('/hardy-weinber-page')
    def redirection():
        return redirect(url_for('hardy_weinberg.hardy_weinberg_page'))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error_pages/404.html", title="404 Page not found!")

    @app.errorhandler(403)
    def page_forbidden(e):
        return render_template("error_pages/403.html", title="403 Page forbidden")

    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow(), 'css_js_ver': 1.12}

    @app.after_request
    def add_header(response):
        if "text/html" in response.content_type:
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            response.headers['Cache-Control'] = 'public, max-age=0'
            return response

        response.cache_control.max_age = 31536000
        return response

    return app


def register_blueprints(app):
    """ Register application blueprints

    :param app: instance of the flask application
    :type app: Flask
    """

    from app.home.views import home
    from app.materials_and_methods.views import materials_and_methods
    from app.about.views import about
    from app.hardy_weinberg.views import hardy_weinberg
    from app.chi_square.views import chi_square
    from app.pic.views import pic
    from app.genetic_distance.views import genetic_distance
    from app.sequences_analysis_tools.views import sequences_analysis_tools
    from app.contact.views import contact
    from app.donors.views import donors
    from app.newsletter.views import newsletter
    from app.userpanel.views import userpanel
    from app.customer_calculation.views import customer_calculation
    from app.privacy_policy.views import privacy_policy
    from app.apmc.views import apmc

    app.register_blueprint(home)
    app.register_blueprint(materials_and_methods)
    app.register_blueprint(about)
    app.register_blueprint(hardy_weinberg)
    app.register_blueprint(chi_square)
    app.register_blueprint(pic)
    app.register_blueprint(genetic_distance)
    app.register_blueprint(sequences_analysis_tools)
    app.register_blueprint(contact)
    app.register_blueprint(donors)
    app.register_blueprint(newsletter)
    app.register_blueprint(userpanel)
    app.register_blueprint(customer_calculation)
    app.register_blueprint(privacy_policy)
    app.register_blueprint(apmc)


def register_jinja_templte_filters(app):
    """Register jinja template filters

    :param app: instance of the flask application
    :type app: Flask
    """

    from app.common.template_filters import to_dict, translate_name, remove_first_last_double_quotes

    app.jinja_env.filters['to_dict'] = to_dict
    app.jinja_env.filters['translate_name'] = translate_name
    app.jinja_env.filters['rm_quotes'] = remove_first_last_double_quotes
