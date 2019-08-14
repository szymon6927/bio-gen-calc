from tests.integration.constants import URL


def test_get_home(test_client):
    response = test_client.get(URL.HOME_GET)
    assert response.status_code == 200
    assert b'Gene-Calc' in response.data
