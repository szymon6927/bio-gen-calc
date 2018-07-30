from flask import render_template, request, jsonify
from . import pic
# from .utils import Codominant, Dominant
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
    data = request.json
    co_d = Codominant(data)
    result = co_d.calculate()
    return jsonify({'data': result})


@pic.route('/pic/send-dominant', methods=['POST'])
def pic_dominant():
    data = request.json
    do = Dominant(data)
    result = do.calculate()
    return jsonify({'data': result})