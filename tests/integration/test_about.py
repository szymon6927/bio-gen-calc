from tests.integration.constants import URL


def test_get_about_ok(test_client):
    response = test_client.get(URL.ABOUT_GET)
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Szymon Miks' in response.data
    assert b'Jan' in response.data
