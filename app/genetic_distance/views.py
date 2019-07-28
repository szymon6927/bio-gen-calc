from flask import render_template, request, jsonify, abort, Response

from app.genetic_distance import genetic_distance
from app.genetic_distance.utils.StandardDistance import StandardDistance
from app.genetic_distance.utils.GeometricDistance import GeometricDistance
from app.genetic_distance.utils.TakezakiNeiDistance import TakezakiNeiDistance

from app.userpanel.models import Page

from app.helpers.db_helper import add_calculation
from app.helpers.db_helper import add_customer_activity
from app.helpers.constants import GENETIC_DISTANCE


@genetic_distance.route('/genetic-distance')
@add_customer_activity
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
                'matrix': gen_distance.redner_matrix()
            }
        })
    except TypeError as e:
        abort(Response(f'Please check type of input data. {str(e)}', 409))
    except ValueError as e:
        abort(Response(f'The quantity or quality of the data is inappropriate! {str(e)}', 409))
    except Exception as e:
        abort(Response(str(e), 400))


@genetic_distance.context_processor
def inject():
    return {
        'module_desc': Page.query.filter_by(slug=request.path).first()
    }

