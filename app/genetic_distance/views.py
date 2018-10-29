from flask import render_template, request, jsonify, abort, Response
from . import genetic_distance
from .utils.StandardDistance import StandardDistance
from .utils.GeometricDistance import GeometricDistance
from .utils.TakezakiNeiDistance import TakezakiNeiDistance

from ..helpers.db_helper import add_calculation
from ..helpers.constants import GENETIC_DISTANCE


@genetic_distance.route('/genetic-distance')
def genetic_distance_page():
    return render_template('genetic_distance/index.html', title="Estimation of Genetic Distance")


@genetic_distance.route('/genetic-distance/send-data-distance', methods=['POST'])
def get_data():
    try:
        data = request.get_json()
        distance_choice = data.get("type_of_distance")

        distance_type = {
            'standard': StandardDistance(data),
            'geometric': GeometricDistance(data),
            'takezaki-nei': TakezakiNeiDistance(data)
        }

        gen_distance = distance_type[distance_choice]
        gen_distance.calcuate_distances()
        gen_distance.build_matrix()

        add_calculation(module_name=f'{GENETIC_DISTANCE}_{distance_choice}',
                        user_data=data, result=gen_distance.get_matrix().tolist(), ip_address=request.remote_addr)

        return jsonify({
            'data': {
                'dendro_base64': gen_distance.render_dendrogram(),
                'matrix_latex': gen_distance.redner_matrix()
            }
        })
    except TypeError as e:
        abort(Response(f'Please check type of input data. {str(e)}', 409))
    except ValueError as e:
        abort(Response(f'The quantity or quality of the data is inappropriate! {str(e)}', 409))
    except Exception as e:
        abort(Response(str(e), 400))

