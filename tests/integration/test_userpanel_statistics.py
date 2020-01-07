from tests.integration.constants import URL
from tests.integration.utils import create_anonymous_calculations
from tests.integration.utils import create_calculations
from tests.integration.utils import create_customer
from tests.integration.utils import create_superuser_customer
from tests.integration.utils import login_customer


def test_get_statistics_all_calculations(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    calculations = create_anonymous_calculations()

    response = test_client.get(URL.USERPANEL_STATISTICS_ALL_CALCULATIONS)

    assert response.status_code == 200

    for calculation in calculations:
        assert calculation.get('module_name').encode() in response.data


def test_get_statistics_all_customers_calculations(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    calculations = create_calculations(customer)

    response = test_client.get(URL.USERPANEL_STATISTICS_ALL_CUSTOMERS_CALCULATIONS)

    assert response.status_code == 200

    for calculation in calculations:
        assert calculation.get('title').encode() in response.data


def test_get_statistics_all_calculations_with_normal_customer(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_STATISTICS_ALL_CALCULATIONS)

    assert response.status_code == 200
    assert b'You do not have access here!' in response.data


def test_get_statistics_all_customers_calculations_with_normal_customer(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_STATISTICS_ALL_CUSTOMERS_CALCULATIONS)

    assert response.status_code == 200
    assert b'You do not have access here!' in response.data


def test_get_statistics_all_models(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_STATISTICS_ALL_MODELS)

    assert response.status_code == 200
    assert b'All models' in response.data


def test_get_statistics_all_models_with_normal_customer(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_STATISTICS_ALL_MODELS)

    assert response.status_code == 200
    assert b'You do not have access here!' in response.data
