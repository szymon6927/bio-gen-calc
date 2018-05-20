from flask import render_template, request, jsonify
from . import pic
from .utils import Codominant


@pic.route('/pic')
def pic_page():
    """
    Render the pic & h template
    """
    return render_template('pic/index.html', title="Polymorphic information content & Heterozygosity")


@pic.route('/sendCodominant', methods=['POST'])
def pic_codominant():
    data = request.json
    print(data, flush=True)
    co_d = Codominant(data)
    co_d.calcuate_pic()

    return jsonify({'result': data})
