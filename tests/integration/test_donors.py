from tests.integration.constants import URL


def test_get_donors_ok(test_client):
    response = test_client.get(URL.DONORS_GET)
    assert response.status_code == 200
    assert b'Our donors' in response.data
