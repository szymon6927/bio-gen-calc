from tests.integration.constants import URL
from tests.integration.utils import create_customer
from tests.integration.utils import create_superuser_customer
from tests.integration.utils import get_pages_fixture
from tests.integration.utils import login_customer


def test_get_pages_with_super_customer(test_client):
    super_customer, plain_password = create_superuser_customer()
    login_customer(test_client, super_customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_PAGES_GET)

    pages_fixture = get_pages_fixture()

    for page_fixture in pages_fixture:
        assert page_fixture.get('slug') in response.data.decode()

    assert response.status_code == 200


def test_get_pages_with_normal_customer(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_PAGES_GET)

    assert response.status_code == 200
    assert b'You do not have access here!' in response.data


def test_get_page_details(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    pages_fixture = get_pages_fixture()

    for page_fixture in pages_fixture:
        response = test_client.get(f"{URL.USERPANEL_PAGE_DETAILS_GET}{page_fixture.get('id')}")

        assert response.status_code == 200


def test_post_page_details(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    pages_fixture = get_pages_fixture()

    for i, page_fixture in enumerate(pages_fixture):
        data = dict()
        data['name'] = f"Test Name {i}"

        response = test_client.post(
            f"{URL.USERPANEL_PAGE_DETAILS_POST}{page_fixture.get('id')}", data=data, follow_redirects=True
        )

        assert response.status_code == 200
        assert b'You have successfully edited the page' in response.data


def test_get_page_add(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_PAGE_ADD_GET)

    assert response.status_code == 200
    assert b'Add new page' in response.data


def test_post_page_add(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    data = dict()
    data['name'] = "New page"

    response = test_client.post(URL.USERPANEL_PAGE_ADD_GET, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'You have successfully added the page' in response.data
    assert data['name'] in response.data.decode()


def test_get_page_delete(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    pages_fixture = get_pages_fixture()

    for page_fixture in pages_fixture:
        response = test_client.get(f"{URL.USERPANEL_PAGE_DELETE_GET}{page_fixture.get('id')}", follow_redirects=True)

        assert response.status_code == 200
        assert b'You have successfully delete the page' in response.data
