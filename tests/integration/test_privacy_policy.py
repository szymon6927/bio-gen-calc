from tests.integration.constants import URL


def test_get_privacy_policy_ok(test_client):
    response = test_client.get(URL.PRIVACY_POLICY_GET)

    assert response.status_code == 200
    assert b'Privacy policy' in response.data
