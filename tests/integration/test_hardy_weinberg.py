import json

from app.common.constants import ModuleName
from app.userpanel.models import Calculation
from tests.integration.constants import URL


def test_get_hardy_weinberg_ok(test_client):
    response = test_client.get(URL.HARDY_WEINBERG_GET)
    assert response.status_code == 200
    assert b'Hardy-Weinberg equilibrium' in response.data


def test_post_hardy_weinberg_ok(test_client):
    data = dict()
    data["ho"] = 4
    data["he"] = 3
    data["rho"] = 2
    data["alfa"] = 0.05

    response = test_client.post(URL.HARDY_WEINBERG_POST, data=json.dumps(data), content_type='application/json')
    calculation = Calculation.query.first()

    assert response.status_code == 200
    assert ModuleName.HARDY_WEINBERG in calculation.module_name
