from tests.integration.constants import URL


def test_get_materials_and_methods(test_client):
    response = test_client.get(URL.MATERIALS_AND_METHODS_GET)
    assert response.status_code == 200
    assert b'Materials' in response.data  # workaround for & character
    assert b'Methods' in response.data  # workaround for & character
