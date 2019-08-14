from tests.integration.constants import URL


def test_get_contact(test_client):
    response = test_client.get(URL.CONTACT_GET)
    assert response.status_code == 200
    assert b'Contact Us' in response.data


def test_post_contact_from_ok(test_client):
    data = {'name': "John", 'email': "test@test.com", 'message': "test message"}

    response = test_client.post(URL.CONTACT_POST, data=data)
    assert response.status_code == 302


def test_post_contact_form_empty_data(test_client):
    response = test_client.post(URL.CONTACT_POST)

    assert response.status_code == 200
    assert b'This field is required' in response.data


def test_post_contact_form_empty_name(test_client):
    data = {'name': "", 'email': "test@test.com", 'message': "test message"}

    response = test_client.post(URL.CONTACT_POST, data=data)

    assert response.status_code == 200
    assert b'This field is required' in response.data


def test_post_contact_form_empty_email(test_client):
    data = {'name': "John", 'email': "", 'message': "test message"}

    response = test_client.post(URL.CONTACT_POST, data=data)

    assert response.status_code == 200
    assert b'This field is required' in response.data


def test_post_contact_form_empty_message(test_client):
    data = {'name': "John", 'email': "test@test.com", 'message': ""}

    response = test_client.post(URL.CONTACT_POST, data=data)

    assert response.status_code == 200
    assert b'This field is required' in response.data


def test_post_contact_form_invalid_email(test_client):
    data = {'name': "John", 'email': "john@test123", 'message': "test message"}

    response = test_client.post(URL.CONTACT_POST, data=data)

    assert response.status_code == 200
    assert b'Invalid email address' in response.data
