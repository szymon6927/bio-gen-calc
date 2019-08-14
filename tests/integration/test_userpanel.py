from io import BytesIO
from unittest.mock import patch

from app.customer_calculation.models import CustomerCalculation
from app.userpanel.models import Customer
from tests.integration.constants import URL
from tests.integration.utils import create_calculations
from tests.integration.utils import create_customer
from tests.integration.utils import create_superuser_customer
from tests.integration.utils import get_pages_fixture
from tests.integration.utils import login_customer


def test_get_login_ok(test_client):
    response = test_client.get(URL.USERPANEL_LOGIN_GET)

    assert response.status_code == 200
    assert b'Login to your account' in response.data


def test_post_login_with_login_ok(test_client):
    customer, plain_password = create_customer()

    data = dict()
    data['login_or_email'] = customer.login
    data['password'] = plain_password

    response = test_client.post(URL.USERPANEL_LOGIN_POST, data=data, follow_redirects=True)
    customers = Customer.query.all()

    assert response.status_code == 200
    assert len(customers) == 1
    assert b'Dashboard' in response.data


def test_post_login_with_email_ok(test_client):
    customer, plain_password = create_customer()

    data = dict()
    data['login_or_email'] = customer.email
    data['password'] = plain_password

    response = test_client.post(URL.USERPANEL_LOGIN_POST, data=data, follow_redirects=True)
    customers = Customer.query.all()

    assert response.status_code == 200
    assert len(customers) == 1
    assert b'Dashboard' in response.data


def test_post_login_no_customer(test_client):
    data = dict()
    data['login_or_email'] = "test"
    data['password'] = "test123test123"

    response = test_client.post(URL.USERPANEL_LOGIN_POST, data=data, follow_redirects=True)
    customers = Customer.query.all()

    assert response.status_code == 200
    assert len(customers) == 0
    assert b'Invalid username or password' in response.data


def test_post_login_too_short_password(test_client):
    data = dict()
    data['login_or_email'] = "test"
    data['password'] = "test123"

    response = test_client.post(URL.USERPANEL_LOGIN_POST, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'Field must be between 8 and 80 characters long' in response.data


def test_get_logout_ok(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_LOGOUT_GET, follow_redirects=True)

    assert response.status_code == 200
    assert b'Login to your account' in response.data


def test_get_logout_when_user_not_logged_in(test_client):
    response = test_client.get(URL.USERPANEL_LOGOUT_GET, follow_redirects=True)

    assert response.status_code == 200
    assert b'Login to your account' in response.data


def test_get_register_ok(test_client):
    response = test_client.get(URL.USERPANEL_REGISTER_GET)

    assert response.status_code == 200
    assert b'Register for an account' in response.data


def test_post_register_ok(test_client):
    data = dict()
    data['first_name'] = "John"
    data['last_name'] = "Done"
    data['login'] = "john_done"
    data['email'] = "john_done@mail.com"
    data['password'] = "test123test123"
    data['password_confirm'] = "test123test123"

    response = test_client.post(URL.USERPANEL_REGISTER_POST, data=data, follow_redirects=True)
    customers = Customer.query.all()

    assert response.status_code == 200
    assert len(customers) == 1
    assert b'Dashboard' in response.data


def test_post_register_without_email(test_client):
    data = dict()
    data['first_name'] = "John"
    data['last_name'] = "Done"
    data['login'] = "john_done"
    data['email'] = ""
    data['password'] = "test123test123"
    data['password_confirm'] = "test123test123"

    response = test_client.post(URL.USERPANEL_REGISTER_POST, data=data, follow_redirects=True)
    customers = Customer.query.all()

    assert response.status_code == 200
    assert len(customers) == 0
    assert b'This field is required' in response.data


def test_post_register_without_login(test_client):
    data = dict()
    data['first_name'] = "John"
    data['last_name'] = "Done"
    data['login'] = ""
    data['email'] = "john_done@mail.com"
    data['password'] = "test123test123"
    data['password_confirm'] = "test123test123"

    response = test_client.post(URL.USERPANEL_REGISTER_POST, data=data, follow_redirects=True)
    customers = Customer.query.all()

    assert response.status_code == 200
    assert len(customers) == 0
    assert b'This field is required' in response.data


def test_post_register_without_password_confirmation(test_client):
    data = dict()
    data['first_name'] = "John"
    data['last_name'] = "Done"
    data['login'] = "john_done"
    data['email'] = "john_done@mail.com"
    data['password'] = "test123test123"

    response = test_client.post(URL.USERPANEL_REGISTER_POST, data=data, follow_redirects=True)
    customers = Customer.query.all()

    assert response.status_code == 200
    assert len(customers) == 0
    assert b'Passwords must match' in response.data


def test_post_register_with_login_which_already_exist(test_client):
    customer, plain_password = create_customer()

    data = dict()
    data['login'] = customer.login
    data['email'] = "john_done@mail.com"
    data['password'] = "test123test123"
    data['password_confirm'] = "test123test123"

    response = test_client.post(URL.USERPANEL_REGISTER_POST, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'That login is taken. Please choose a different one.' in response.data


def test_post_register_with_email_which_already_exist(test_client):
    customer, plain_password = create_customer()

    data = dict()
    data['login'] = "john_done"
    data['email'] = customer.email
    data['password'] = "test123test123"
    data['password_confirm'] = "test123test123"

    response = test_client.post(URL.USERPANEL_REGISTER_POST, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'That email is taken. Please choose a different one.' in response.data


def test_get_userpanel(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_GET, follow_redirects=True)

    assert response.status_code == 200
    assert b'Dashboard' in response.data


def test_get_userpanel_when_user_not_logged_in(test_client):
    response = test_client.get(URL.USERPANEL_GET, follow_redirects=True)

    assert response.status_code == 200
    assert b'Login to your account' in response.data


def test_get_dashboard(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_DASHBOARD_GET)

    assert response.status_code == 200
    assert customer.login in response.data.decode()
    assert 'Total calculations' in response.data.decode()
    assert 'Total visits' in response.data.decode()


def test_get_dashboard_when_user_not_logged_in(test_client):
    response = test_client.get(URL.USERPANEL_DASHBOARD_GET, follow_redirects=True)

    assert response.status_code == 200
    assert b'Login to your account' in response.data


def test_get_edit_profile(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_EDITPROFILE_GET)

    assert response.status_code == 200
    assert b'Edit profile' in response.data


def test_post_edit_profile_edit_first_and_last_name(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    data = dict()
    data['first_name'] = "Other First Name"
    data['last_name'] = "Other Last Name"
    data['password'] = plain_password
    data['password_confirm'] = plain_password

    response = test_client.post(URL.USERPANEL_EDITPROFILE_POST, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'You have successfully edited the profile' in response.data
    assert customer.first_name == data['first_name']
    assert customer.last_name == data['last_name']


def test_post_edit_profile_change_password(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    old_password = customer.password

    data = dict()
    data['password'] = "new_password_123"
    data['password_confirm'] = "new_password_123"

    response = test_client.post(URL.USERPANEL_EDITPROFILE_POST, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'You have successfully edited the profile' in response.data
    assert customer.password != old_password


def test_post_edit_profile_password_must_match(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    data = dict()
    data['password'] = "new_password_123"
    data['password_confirm'] = "new_password"

    response = test_client.post(URL.USERPANEL_EDITPROFILE_POST, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'Passwords must match' in response.data


@patch('app.helpers.file_helper.Image')
def test_post_edit_profile_upload_profile_pic(image_mock, test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    old_profile_pic = customer.profile_pic

    image_mock.save.return_value = True

    data = dict()
    data['picture'] = (BytesIO(b'test_image_data'), 'test_file.jpg')
    data['password'] = plain_password
    data['password_confirm'] = plain_password

    response = test_client.post(
        URL.USERPANEL_EDITPROFILE_POST, data=data, content_type='multipart/form-data', follow_redirects=True
    )

    assert response.status_code == 200
    assert b'You have successfully edited the profile' in response.data
    assert old_profile_pic != customer.profile_pic


def test_post_edit_profile_upload_profile_pic_with_wrong_file_extension(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    old_profile_pic = customer.profile_pic

    data = dict()
    data['picture'] = (BytesIO(b'test_image_data'), 'test_file.pdf')
    data['password'] = plain_password
    data['password_confirm'] = plain_password

    response = test_client.post(
        URL.USERPANEL_EDITPROFILE_POST, data=data, content_type='multipart/form-data', follow_redirects=True
    )

    assert response.status_code == 200
    assert b'File does not have an approved extension: jpg, png, jpeg' in response.data
    assert old_profile_pic == customer.profile_pic


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

    assert response.status_code == 403


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
