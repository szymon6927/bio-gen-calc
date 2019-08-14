import json

from app.common.constants import ModuleName
from app.userpanel.models import Calculation
from tests.integration.constants import URL


def test_get_pic_ok(test_client):
    response = test_client.get(URL.PIC_GET)
    assert response.status_code == 200
    assert b'Polymorphic information content' in response.data


def test_post_pic_dominant_ok(test_client):
    data = dict()
    data["amplified_marker"] = 2
    data["absecnce_marker"] = 3

    response = test_client.post(URL.PIC_DOMINANT_POST, data=json.dumps(data), content_type='application/json')
    calculation = Calculation.query.first()

    assert response.status_code == 200
    assert ModuleName.PIC_DOMINANT in calculation.module_name


def test_post_pic_dominant_invalid_data(test_client):
    data = dict()
    data["amplified_marker"] = 2
    data["absecnce_marker"] = "test"

    response = test_client.post(URL.PIC_DOMINANT_POST, data=json.dumps(data), content_type='application/json')
    calculations = Calculation.query.all()

    assert response.status_code == 400
    assert len(calculations) == 0


def test_post_pic_codominant_ok(test_client):
    data = dict()
    data["count"] = 3
    data["allele-0"] = 4
    data["allele-1"] = 2
    data["allele-2"] = 3

    response = test_client.post(URL.PIC_CODOMINANT_POST, data=json.dumps(data), content_type='application/json')
    calculation = Calculation.query.first()

    assert response.status_code == 200
    assert ModuleName.PIC_CODOMINANT in calculation.module_name


def test_post_pic_codominant_invalid_data(test_client):
    data = dict()
    data["count"] = 2
    data["allele-0"] = "0.0.1"
    data["allele-1"] = "0.01"

    response = test_client.post(URL.PIC_CODOMINANT_POST, data=json.dumps(data), content_type='application/json')

    calculations = Calculation.query.all()

    assert response.status_code == 400
    assert len(calculations) == 0


def test_post_pic_codominant_mixed_type_or_sum_of_alleles(test_client):
    data = dict()
    data["count"] = 2
    data["allele-0"] = 0.01
    data["allele-1"] = 0.01

    response = test_client.post(URL.PIC_CODOMINANT_POST, data=json.dumps(data), content_type='application/json')

    calculations = Calculation.query.all()

    assert response.status_code == 400
    assert len(calculations) == 0
    assert b'Mixed type of input values or sum of alleles frequencies not equal to 0' in response.data
