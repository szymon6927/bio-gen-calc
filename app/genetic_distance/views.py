from flask import render_template, request, jsonify
from . import genetic_distance
from .utils import GeneticDistance


@genetic_distance.route('/genetic-distance')
def genetic_distance_page():
    return render_template('genetic_distance/index.html', title="Estimation of Genetic Distance")


@genetic_distance.route('/genetic-distance/send-data-distance', methods=['POST'])
def get_data():
    data = request.get_json()
    gen_distance = GeneticDistance(data)
    gen_distance.calcuate_distances()
    gen_distance.build_matrix()

    return jsonify({
            'data': {
                'dendro_base64': gen_distance.render_dendrogram(),
                'matrix_latex': gen_distance.redner_matrix()
            }
            })
