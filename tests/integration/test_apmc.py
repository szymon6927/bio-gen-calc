from tests.integration.constants import URL
from tests.integration.utils import create_customer
from tests.integration.utils import login_customer


def test_get_apmc_ok(test_client):
    response = test_client.get(URL.APMC_GET)

    assert response.status_code == 200
    assert b'APMC' in response.data


def test_get_apmc_as_not_logged_in_user(test_client):
    response = test_client.get(URL.APMC_GET)

    assert response.status_code == 200
    assert b'You have to be logged in' in response.data


def test_get_apmc_as_logged_in_user(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.APMC_GET)

    assert response.status_code == 200
    assert b'Your project name' in response.data
    assert b'Click to upload file' in response.data
    assert b'Pre-train' in response.data


def test_get_apmc_how_to_use_ok(test_client):
    response = test_client.get(URL.APMC_HOW_TO_USE_GET)

    assert response.status_code == 200
    assert b'How to use' in response.data


def test_get_apmc_documentation_ok(test_client):
    response = test_client.get(URL.APMC_DOCUMENTATION_GET)

    assert response.status_code == 200
    assert b'Documentation' in response.data
