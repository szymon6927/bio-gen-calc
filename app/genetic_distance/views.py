from flask import render_template, request, jsonify, abort, Response
from . import genetic_distance
from .utils.StandardDistance import StandardDistance
from .utils.GeometricDistance import GeometricDistance
from .utils.TakezakiNeiDistance import TakezakiNeiDistance


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

        return jsonify({
            'data': {
                'dendro_base64': gen_distance.render_dendrogram(),
                'matrix_latex': gen_distance.redner_matrix()
            }
        })
    except TypeError:
        abort(Response("Please check type of input data", 409))
    except ValueError:
        abort(Response("The quantity or quality of the data is inappropriate!", 409))
    except Exception as e:
        abort(Response(str(e), 400))

