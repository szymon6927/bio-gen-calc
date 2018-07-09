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
    return jsonify({'data': data})
