from io import BytesIO
from unittest.mock import patch

from tests.integration.constants import URL
from tests.integration.utils import create_customer
from tests.integration.utils import login_customer


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
