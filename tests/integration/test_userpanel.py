from app.userpanel.models import Customer
from tests.integration.constants import URL
from tests.integration.utils import create_customer
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
