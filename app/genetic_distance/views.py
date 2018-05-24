from flask import render_template
from . import genetic_distance


@genetic_distance.route('/genetic-distance')
def genetic_distance_page():
    return render_template('genetic_distance/index.html', title="Estimation of Genetic Distance")
