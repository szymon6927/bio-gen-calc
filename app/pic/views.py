from flask import render_template, request, jsonify, abort, Response
from . import pic
from .utils.CodominantCalculation import Codominant
from .utils.DominantCalculation import Dominant


@pic.route('/pic')
def pic_page():
    """
    Render the pic & h template
    """
    return render_template('pic/index.html', title="Polymorphic information content & Heterozygosity")


@pic.route('/pic/send-codominant', methods=['POST'])
def pic_codominant():
    try:
        data = request.json
        co_d = Codominant(data)
        result = co_d.calculate()
        return jsonify({'data': result})
    except TypeError:
        abort(Response("Please check type of input data", 409))
    except Exception as e:
        abort(Response(str(e), 400))


@pic.route('/pic/send-dominant', methods=['POST'])
def pic_dominant():
    try:
        data = request.json
        do = Dominant(data)
        result = do.calculate()
        return jsonify({'data': result})
    except TypeError:
        abort(Response("Please check type of input data", 409))
    except Exception as e:
        abort(Response(str(e), 400))