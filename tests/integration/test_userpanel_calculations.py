from app.customer_calculation.models import CustomerCalculation
from tests.integration.constants import URL
from tests.integration.utils import create_calculations
from tests.integration.utils import create_customer
from tests.integration.utils import login_customer


def test_get_calculation_view(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    calculations = create_calculations(customer)

    response = test_client.get(URL.USERPANEL_CALCULATIONS_GET)

    assert response.status_code == 200

    for calculation in calculations:
        assert calculation.get('title').encode() in response.data


def test_get_calculation_search_view(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    calculations = create_calculations(customer)

    for calculation in calculations:
        calculation_title = calculation.get('title')
        response = test_client.get(f'{URL.USERPANEL_CALCULATIONS_SEARCH_GET}?query={calculation_title}')

        assert response.status_code == 200
        assert 'Results for query:'.encode() in response.data
        assert f'{calculation_title}'.encode() in response.data
        assert f'Title: {calculation_title}'.encode() in response.data


def test_get_calculation_delete(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    _ = create_calculations(customer)

    calculation_id = 1
    response = test_client.get(f'{URL.USERPANEL_CALCULATIONS_DELETE}{calculation_id}', follow_redirects=True)

    calculations = CustomerCalculation.query.all()

    assert response.status_code == 200
    assert b'You have successfully deleted the calculation' in response.data
    assert len(calculations) == 2


def test_get_calculation_details(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    _ = create_calculations(customer)

    calculation_id = 1
    response = test_client.get(f'{URL.USERPANEL_CALCULATION_DETAILS_GET}{calculation_id}')

    assert response.status_code == 200
    assert b'Calculation details' in response.data
    assert b'Input' in response.data
    assert b'Result' in response.data
