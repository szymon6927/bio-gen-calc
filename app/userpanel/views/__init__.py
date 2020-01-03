from flask import Blueprint


def import_userpanel_views():
    from app.userpanel.views import apmc_views
    from app.userpanel.views import calculations_views
    from app.userpanel.views import customers_views
    from app.userpanel.views import general_views
    from app.userpanel.views import login_logout_register_view
    from app.userpanel.views import ncbi_scrapper_views
    from app.userpanel.views import pages_views
    from app.userpanel.views import statistics_views


userpanel = Blueprint('userpanel', __name__)
import_userpanel_views()
