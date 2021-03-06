from flask import Blueprint
from flask import Response
from flask import abort
from flask import jsonify
from flask import render_template
from flask import request

from app.clients.slack_client import SlackNotification
from app.common.constants import ModuleName
from app.common.decorators import add_customer_activity
from app.helpers.db_helper import add_calculation
from app.pic.ds.CodominantCalculation import Codominant
from app.pic.ds.DominantCalculation import Dominant
from app.userpanel.models import Page

slack_notification = SlackNotification()
pic = Blueprint('pic', __name__)


@pic.route('/pic')
@add_customer_activity
def pic_page():
    return render_template('pic/index.html', title="Polymorphic information content & Heterozygosity")


@pic.route('/pic/send-codominant', methods=['POST'])
def pic_codominant():
    try:
        data = request.get_json()
        co_d = Codominant(data)
        result = co_d.calculate()

        add_calculation(
            module_name=ModuleName.PIC_CODOMINANT, user_data=data, result=result, ip_address=request.remote_addr
        )
        slack_notification.pic_codominant_calculation(data, result, request.remote_addr)

        return jsonify({'data': result})
    except TypeError as e:
        abort(Response(f'Please check type of input data. {e}', 422))
    except Exception as e:
        abort(Response(str(e), 400))


@pic.route('/pic/send-dominant', methods=['POST'])
def pic_dominant():
    try:
        data = request.get_json()
        do = Dominant(data)
        result = do.calculate()

        add_calculation(
            module_name=ModuleName.PIC_DOMINANT, user_data=data, result=result, ip_address=request.remote_addr
        )
        slack_notification.pic_dominant_calculation(data, result, request.remote_addr)

        return jsonify({'data': result})
    except TypeError as e:
        abort(Response(f'Please check type of input data. {e}', 422))
    except Exception as e:
        abort(Response(str(e), 400))


@pic.context_processor
def inject():
    return {'module_desc': Page.query.filter_by(slug=request.path).first()}
