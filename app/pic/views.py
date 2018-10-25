from flask import render_template, request, jsonify, abort, Response
from . import pic
from .utils.CodominantCalculation import Codominant
from .utils.DominantCalculation import Dominant

from ..helpers.db_helper import add_calculation
from ..helpers.constants import PIC_CODOMINANT, PIC_DOMINANT


@pic.route('/pic')
def pic_page():
    """
    Render the pic & h template
    """
    return render_template('pic/index.html', title="Polymorphic information content & Heterozygosity")


@pic.route('/pic/send-codominant', methods=['POST'])
def pic_codominant():
    try:
        data = request.get_json()
        co_d = Codominant(data)
        result = co_d.calculate()

        add_calculation(module_name=PIC_CODOMINANT, user_data=data, result=result, ip_address=request.remote_addr)

        return jsonify({'data': result})
    except TypeError as e:
        abort(Response(f'Please check type of input data. {e}', 409))
    except Exception as e:
        abort(Response(str(e), 400))


@pic.route('/pic/send-dominant', methods=['POST'])
def pic_dominant():
    try:
        data = request.get_json()
        do = Dominant(data)
        result = do.calculate()

        add_calculation(module_name=PIC_DOMINANT, user_data=data, result=result, ip_address=request.remote_addr)

        return jsonify({'data': result})
    except TypeError as e:
        abort(Response(f'Please check type of input data. {e}', 409))
    except Exception as e:
        abort(Response(str(e), 400))
