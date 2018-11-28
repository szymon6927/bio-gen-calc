# app/__init__.py

from datetime import datetime
import pdfkit
import base64

from flask import Flask, render_template, request, make_response, abort, Response, send_from_directory

from flask_htmlmin import HTMLMIN
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_compress import Compress

from .database import db
from .models.Admin import User, Page
from .models.Userpanel import Customer

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
    register_jinja_templte_filters(app)

    login_manager.init_app(app)
    login_manager.login_view = 'userpanel.login'

    Compress(app)
    HTMLMIN(app)

    @login_manager.user_loader
    def load_customer(obj_id):
        if request.path.startswith("/admin"):
            return User.query.get(int(obj_id))
        else:
            return Customer.query.get(int(obj_id))

    @app.route('/robots.txt')
    @app.route('/sitemap.xml')
    def serve_static_seo_files():
        return send_from_directory(app.static_folder, request.path[1:])

    @app.route('/generate-pdf', methods=['POST'])
    def generate_pdf():
        try:
            data = request.get_json()

            template = render_template('utils/pdf_template.html', content=data['content'])
            css = ['app/static/css/vendors/bootstrap.min.css',
                   'app/static/css/style.css',
                   'app/static/css/pdf-style.css'
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

    @app.errorhandler(404)
    def page_not_found(e):
        print(e)
        return render_template("404.html", title="404 Page not found!")

    @app.context_processor
    def inject_now():
        return {
            'now': datetime.utcnow(),
            'module_desc': Page.query.filter_by(breadcrumbs=request.path).first(),
            'css_js_ver': 1.11
        }

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
    from .home import home
    from .materials_and_methods import materials_and_methods
    from .about import about
    from .hardy_weinber import hardy_weinber
    from .chi_square import chi_square
    from .pic import pic
    from .genetic_distance import genetic_distance
    from .sequences_analysis_tools import sequences_analysis_tools
    from .contact import contact
    from .donors import donors
    from .newsletter import newsletter
    from .userpanel import userpanel
    from .customer_calculation import customer_calculation
    from .privacy_policy import privacy_policy

    app.register_blueprint(home)
    app.register_blueprint(materials_and_methods)
    app.register_blueprint(about)
    app.register_blueprint(hardy_weinber)
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


def register_jinja_templte_filters(app):
    from .helpers.template_filters import to_dict, translate_name

    app.jinja_env.filters['to_dict'] = to_dict
    app.jinja_env.filters['translate_name'] = translate_name
