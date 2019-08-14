import json

from sqlalchemy import desc

from app.common.constants import ModuleName
from app.userpanel.models import Calculation
from tests.integration.constants import URL


def test_get_genetic_distance_ok(test_client):
    response = test_client.get(URL.GENETIC_DISTANCE_GET)
    assert response.status_code == 200
    assert b'Genetic Distance' in response.data


def test_post_genetic_distance_all_types_all_dendro_ok(test_client):
    data = dict()
    data['taxon_number'] = "6"
    data['locus_number'] = "1"
    data['number_of_alleles'] = [2]
    data['column_0'] = [0.3, 0.7]
    data['column_1'] = [0.4, 0.6]
    data['column_2'] = [0.5, 0.5]
    data['column_3'] = [0.6, 0.4]
    data['column_4'] = [0.7, 0.3]
    data['column_5'] = [0.8, 0.2]

    genetic_distance_types = ["standard", "geometric", "takezaki-nei"]
    dendrogram_types = ["upgma", "wpgma", "upgmc", "wpgmc", "single-linkage", "complete-linkage"]

    for distance_type in genetic_distance_types:
        for dendrogram_type in dendrogram_types:
            data['type_of_distance'] = distance_type
            data['type_of_dendrogram'] = dendrogram_type

            response = test_client.post(
                URL.GENETIC_DISTANCE_POST, data=json.dumps(data), content_type='application/json'
            )

            calculation = Calculation.query.order_by(desc('created_at')).first()
            result = json.loads(response.data)

            assert response.status_code == 200
            assert 'dendro_base64' in result['data']
            assert 'matrix' in result['data']
            assert f'{ModuleName.GENETIC_DISTANCE}_{distance_type}' in calculation.module_name
