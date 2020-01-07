from tests.integration.constants import URL
from tests.integration.utils import create_customer
from tests.integration.utils import create_superuser_customer
from tests.integration.utils import login_customer


def test_get_customers(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    test_customer, _ = create_customer()

    response = test_client.get(URL.USERPANEL_CUSTOMERS_GET)

    assert response.status_code == 200
    assert test_customer.email in response.data.decode()


def test_get_customer_details(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    test_customer, _ = create_customer()

    response = test_client.get(f"{URL.USERPANEL_CUSTOMER_DETAILS_GET}")

    assert response.status_code == 200
    assert test_customer.login in response.data.decode()


def test_post_customer_details(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    test_customer, _ = create_customer()

    data = dict()
    data['first_name'] = "New first name"

    response = test_client.post(
        f"{URL.USERPANEL_CUSTOMER_DETAILS_POST}{test_customer.id}", data=data, follow_redirects=True
    )

    assert response.status_code == 200
    assert b'You have successfully edited the customer.' in response.data
