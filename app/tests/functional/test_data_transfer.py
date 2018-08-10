import json


def test_hw_communiction(test_client):
    data = dict()
    data["ho"] = 4
    data["he"] = 3
    data["rho"] = 2
    data["alfa"] = 0.05

    response = test_client.post('/hardy-weinber/send-data', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200


def test_chi_square_communiction(test_client):
    data = dict()
    data['row-0'] = [4.0, 4.0]
    data['row-1'] = [2.0, 3.0]
    data['column-0'] = [4.0, 2.0]
    data['column-0'] = [4.0, 3.0]
    data['width'] = 2
    data['height'] = 2
    data['field_sum'] = 13

    response = test_client.post('/chi-square/send-data', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200


def test_chi_square_goodnes_communiction(test_client):
    data = dict()
    data['observed'] = [4.0, 3.0, 2.0]
    data['expected'] = [3.0, 2.0, 4.0]

    response = test_client.post('/chi-square/send-data-goodness', data=json.dumps(data),
                                content_type='application/json')

    assert response.status_code == 200


def test_genetic_distance_communiction(test_client):
    data = dict()
    data["taxon_number"] = "6"
    data["locus_number"] = "1"
    data["type_of_distance"] = "standard"
    data["type_of_dendrogram"] = "upgma"
    data["number_of_alleles"] = [2]
    data["column_0"] = [0.3, 0.7]
    data["column_1"] = [0.4, 0.6]
    data["column_2"] = [0.5, 0.5]
    data["column_3"] = [0.6, 0.4]
    data["column_4"] = [0.7, 0.3]
    data["column_5"] = [0.8, 0.2]

    response = test_client.post('/genetic-distance/send-data-distance', data=json.dumps(data),
                                content_type='application/json')

    assert response.status_code == 200


def test_pic_dominant_communiction(test_client):
    data = dict()
    data["amplified_marker"] = 2
    data["absecnce_marker"] = 3

    response = test_client.post('/pic/send-dominant', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 200


def test_pic_codominant_communiction(test_client):
    data = dict()
    data["count"] = 3
    data["allele-0"] = 4
    data["allele-1"] = 2
    data["allele-2"] = 3

    response = test_client.post('/pic/send-codominant', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 200


def test_generate_pdf(test_client):
    data = dict()
    data["content"] = "<h1>TEST</h1>"

    response = test_client.post('/generate-pdf', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert response.mimetype == 'application/pdf'


