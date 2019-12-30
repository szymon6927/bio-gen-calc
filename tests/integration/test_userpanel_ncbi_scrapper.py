from unittest.mock import patch

from app.mail_scrapper.ncbi_scrapper import NCBIObject
from app.mail_scrapper.ncbi_scrapper import NCBIPubScrapper
from tests.integration.constants import URL
from tests.integration.utils import create_customer
from tests.integration.utils import create_superuser_customer
from tests.integration.utils import get_fixture
from tests.integration.utils import login_customer


def test_get_run_scrapper_super_user(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_RUN_SCRAPPER)

    assert response.status_code == 200
    assert b'Run scrapper' in response.data


def test_get_run_scrapper_normal_customer(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_RUN_SCRAPPER)

    assert response.status_code == 200
    assert b'You do not have access here!' in response.data


@patch.object(NCBIPubScrapper, 'run')
def test_post_run_scrapper_super_user(scrapper_mock, test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    scrapper_mock.return_value = [
        NCBIObject(email='test-scrapper@test.com', publication_id='12345', publication_url='testurl')
    ]

    data = {'publication_number': 1, 'mail_package': 1}
    response = test_client.post(URL.USERPANEL_RUN_SCRAPPER, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'Run scrapper' in response.data
    assert b'Successfully added test-scrapper@test.com' in response.data


def test_get_mail_packages_view_superuser(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_ALL_PACKAGES)

    assert b'Mail packages' in response.data
    assert b'Test package 1' in response.data
    assert b'Test package 2' in response.data


def test_get_mail_packages_view_normal_customer(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_ALL_PACKAGES)

    assert response.status_code == 200
    assert b'You do not have access here!' in response.data


def test_get_add_mail_package(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.post(URL.USERPANEL_ADD_PACKAGE)

    assert response.status_code == 200
    assert b'Add new package' in response.data


def test_post_add_mail_package(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    data = {'name': 'Test package name', 'comment': 'Test package comment'}
    response = test_client.post(URL.USERPANEL_ADD_PACKAGE, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'You have successfully added the package' in response.data


def test_post_add_mail_package_without_name(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    data = {'comment': 'Test package comment'}
    response = test_client.post(URL.USERPANEL_ADD_PACKAGE, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'This field is required' in response.data


def test_get_mail_package_details_view_superuser(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    packages_fixture = get_fixture('ncbi_mail_packages.json')

    for package_fixture in packages_fixture:
        response = test_client.get(f"{URL.USERPANEL_PACKAGE_DETAILS}{package_fixture.get('id')}")

        assert response.status_code == 200
        assert b'Edit package' in response.data


def test_get_mail_package_details_view_normal_customer(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    packages_fixture = get_fixture('ncbi_mail_packages.json')

    for package_fixture in packages_fixture:
        response = test_client.get(f"{URL.USERPANEL_PACKAGE_DETAILS}{package_fixture.get('id')}")

        assert b'You do not have access here!' in response.data


def test_post_mail_package_details_view(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    packages_fixture = get_fixture('ncbi_mail_packages.json')

    for i, package_fixture in enumerate(packages_fixture):
        data = dict()
        data['name'] = f"Test Package Name {i}"

        response = test_client.post(
            f"{URL.USERPANEL_PACKAGE_DETAILS}{package_fixture.get('id')}", data=data, follow_redirects=True
        )

        assert response.status_code == 200
        assert b'You have successfully edited the package' in response.data


def test_get_mail_package_csv_export_view(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    packages_fixture = get_fixture('ncbi_mail_packages.json')

    for i, package_fixture in enumerate(packages_fixture):
        response = test_client.get(f"{URL.USERPANEL_PACKAGE_CSV_EXPORT}{package_fixture.get('id')}")

        assert response.status_code == 200
        assert response.mimetype == 'text/csv'


def test_get_mail_package_delete_view(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    packages_fixture = get_fixture('ncbi_mail_packages.json')

    for i, package_fixture in enumerate(packages_fixture):
        response = test_client.get(f"{URL.USERPANEL_PACKAGE_DELETE}{package_fixture.get('id')}", follow_redirects=True)

        assert response.status_code == 200
        assert b'You have successfully delete the package' in response.data


def test_get_all_emails_super_user(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_MAILS_ALL)

    assert response.status_code == 200
    assert b'Scrapped emails' in response.data
    assert b'test1111@test.com' in response.data
    assert b'test1112@test.com' in response.data


def test_get_all_emails_normal_customer(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_MAILS_ALL)

    assert response.status_code == 200
    assert b'You do not have access here!' in response.data


def test_get_add_mail(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.USERPANEL_MAIL_ADD)

    assert response.status_code == 200
    assert b'Add new e-mail' in response.data


def test_post_add_mail(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    data = {
        'email': 'another_test@test.com',
        'ncbi_publication_url': 'test_publication_url',
        'publication_id': 'test_publication_id',
        'mail_package': '1',
    }

    response = test_client.post(URL.USERPANEL_MAIL_ADD, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'You have successfully added the mail to the' in response.data


def test_post_add_mail_with_email_which_already_exist(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    data = {
        'email': 'test1111@test.com',
        'ncbi_publication_url': 'test_publication_url',
        'publication_id': 'test_publication_id',
        'mail_package': '1',
    }

    response = test_client.post(URL.USERPANEL_MAIL_ADD, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'This e-mail is already present in our db in the package' in response.data


def test_post_add_mail_with_empty_email_field(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    data = {
        'email': '',
        'ncbi_publication_url': 'test_publication_url',
        'publication_id': 'test_publication_id',
        'mail_package': '1',
    }

    response = test_client.post(URL.USERPANEL_MAIL_ADD, data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'This field is required' in response.data


def test_get_mail_details_view_superuser(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    mails_fixture = get_fixture('ncbi_mails.json')

    for mail_fixture in mails_fixture:
        response = test_client.get(f"{URL.USERPANEL_MAIL_DETAILS}{mail_fixture.get('id')}")

        assert response.status_code == 200
        assert b'Edit e-mail' in response.data


def test_get_mail_details_view_normal_customer(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    mails_fixture = get_fixture('ncbi_mails.json')

    for mail_fixture in mails_fixture:
        response = test_client.get(f"{URL.USERPANEL_MAIL_DETAILS}{mail_fixture.get('id')}")

        assert b'You do not have access here!' in response.data


def test_post_mail_details_view(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    mails_fixture = get_fixture('ncbi_mails.json')

    for i, mail_fixture in enumerate(mails_fixture):
        data = dict()
        data['email'] = mail_fixture.get('email')
        data['mail_package'] = mail_fixture.get('package_id')
        data['publication_id'] = f"test-publication-id-{i}"

        response = test_client.post(
            f"{URL.USERPANEL_MAIL_DETAILS}{mail_fixture.get('id')}", data=data, follow_redirects=True
        )

        assert response.status_code == 200
        assert b'You have successfully edited the mail' in response.data


def test_get_mail_delete_view(test_client):
    customer, plain_password = create_superuser_customer()
    login_customer(test_client, customer.login, plain_password)

    mails_fixture = get_fixture('ncbi_mails.json')

    for mail_fixture in mails_fixture:
        response = test_client.get(f"{URL.USERPANEL_MAIL_DELETE}{mail_fixture.get('id')}", follow_redirects=True)

        assert response.status_code == 200
        assert b'You have successfully delete the email' in response.data
