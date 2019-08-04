import json

from app.common.constants import ModuleName
from app.userpanel.models import Calculation
from tests.integration.constants import URL


def test_get_chi_square_ok(test_client):
    response = test_client.get(URL.CHI_SQUARE_GET)
    assert response.status_code == 200
    assert b'Chi-Square tests' in response.data


def test_post_chi_square_ok(test_client):
    data = dict()
    data['row-0'] = [4.0, 4.0]
    data['row-1'] = [2.0, 3.0]
    data['column-0'] = [4.0, 2.0]
    data['column-1'] = [4.0, 3.0]
    data['width'] = 2
    data['height'] = 2
    data['field_sum'] = 13

    response = test_client.post(URL.CHI_SQUARE_POST, data=json.dumps(data), content_type='application/json')
    calculation = Calculation.query.first()

    assert response.status_code == 200
    assert ModuleName.CHI_SQUARE in calculation.module_name


def test_post_chi_square_missing_arguments(test_client):
    data = dict()
    data['row-0'] = [4.0, 4.0]
    data['row-1'] = [2.0, 3.0]
    data['column-0'] = [4.0, 2.0]
    data['column-1'] = [4.0, 3.0]
    data['field_sum'] = 13

    response = test_client.post(URL.CHI_SQUARE_POST, data=json.dumps(data), content_type='application/json')
    calculations = Calculation.query.all()

    assert response.status_code == 400
    assert len(calculations) == 0


def test_post_chi_square_invalid_arguments(test_client):
    data = dict()
    data['row-0'] = [4.0]
    data['row-1'] = [2.0, 3.0]
    data['column-0'] = [4.0, 2.0]
    data['column-1'] = [4.0, 3.0]
    data['width'] = 2
    data['height'] = 2
    data['field_sum'] = 13

    response = test_client.post(URL.CHI_SQUARE_POST, data=json.dumps(data), content_type='application/json')
    calculations = Calculation.query.all()

    assert response.status_code == 422
    assert len(calculations) == 0


def test_post_chi_square_goodness_ok(test_client):
    data = dict()
    data['observed'] = [4.0, 3.0, 2.0]
    data['expected'] = [3.0, 2.0, 4.0]

    response = test_client.post(URL.CHI_SQUARE_GOODNESS_POST, data=json.dumps(data), content_type='application/json')
    calculation = Calculation.query.first()

    assert response.status_code == 200
    assert ModuleName.CHI_SQUARE_GOODNESS in calculation.module_name


def test_post_chi_square_goodness_missing_arguments(test_client):
    data = dict()
    data['observed'] = [4.0, 3.0, 2.0]

    response = test_client.post(URL.CHI_SQUARE_GOODNESS_POST, data=json.dumps(data), content_type='application/json')
    calculation = Calculation.query.all()

    assert response.status_code == 400
    assert len(calculation) == 0


def test_post_chi_square_goodness_invalid_arguments(test_client):
    data = dict()
    data['observed'] = [4.0, 3.0, 2.0]
    data['expected'] = [3.0, 2.0, "test"]

    response = test_client.post(URL.CHI_SQUARE_GOODNESS_POST, data=json.dumps(data), content_type='application/json')
    calculation = Calculation.query.all()

    assert response.status_code == 400
    assert len(calculation) == 0
