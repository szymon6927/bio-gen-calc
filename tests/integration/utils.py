import json
import os

from werkzeug.security import generate_password_hash

from app import APP_DIR
from app.common.constants import ModuleName
from app.customer_calculation.models import CustomerCalculation
from app.database import db
from app.userpanel.models import Calculation
from app.userpanel.models import Customer
from tests.integration.constants import URL


def create_customer():
    plain_customer_password = "test123test123test"

    new_customer = Customer()
    new_customer.email = "test@test.com"
    new_customer.login = "test"
    new_customer.password = generate_password_hash(plain_customer_password, method='sha256')
    new_customer.first_name = "John"
    new_customer.last_name = "Done"

    db.session.add(new_customer)
    db.session.commit()

    return new_customer, plain_customer_password


def create_superuser_customer():
    plain_customer_password = "test123test123test"

    super_customer = Customer()
    super_customer.email = "super_test@test.com"
    super_customer.login = "super_test"
    super_customer.password = generate_password_hash(plain_customer_password, method='sha256')
    super_customer.first_name = "Super John"
    super_customer.last_name = "Done"
    super_customer.is_superuser = True

    db.session.add(super_customer)
    db.session.commit()

    return super_customer, plain_customer_password


def login_customer(test_client, login_or_email, password):
    data = dict()
    data['login_or_email'] = login_or_email
    data['password'] = password

    return test_client.post(URL.USERPANEL_LOGIN_POST, data=data, follow_redirects=True)


def create_calculations(logged_customer):
    fake_calculations = [
        {'title': 'HW calculation', 'module_name': ModuleName.HARDY_WEINBERG, 'customer_input': "{}", 'result': "{}"},
        {
            'title': 'PIC dominant calculation',
            'module_name': ModuleName.PIC_DOMINANT,
            'customer_input': "{}",
            'result': "{}",
        },
        {
            'title': 'PIC codominant calculation',
            'module_name': ModuleName.PIC_CODOMINANT,
            'customer_input': "{}",
            'result': "{}",
        },
    ]

    for fake_calculation in fake_calculations:
        calculation = CustomerCalculation(
            customer=logged_customer,
            title=fake_calculation.get('title'),
            module_name=fake_calculation.get('module_name'),
            customer_input=fake_calculation.get('customer_input'),
            result=fake_calculation.get('result'),
        )

        db.session.add(calculation)
        db.session.commit()

    return fake_calculations


def create_anonymous_calculations():
    fake_calculations = [
        {'module_name': ModuleName.HARDY_WEINBERG, 'user_data': "{}", 'result': "{}", 'ip_address': "127.0.0.1"},
        {'module_name': ModuleName.PIC_DOMINANT, 'user_data': "{}", 'result': "{}", 'ip_address': "127.0.0.1"},
        {'module_name': ModuleName.PIC_CODOMINANT, 'user_data': "{}", 'result': "{}", 'ip_address': "127.0.0.1"},
    ]

    for fake_calculation in fake_calculations:
        calculation = Calculation(
            module_name=fake_calculation.get('module_name'),
            user_data=fake_calculation.get('user_data'),
            result=fake_calculation.get('result'),
            ip_address=fake_calculation.get('ip_address'),
        )

        db.session.add(calculation)
        db.session.commit()

    return fake_calculations


def get_pages_fixture():
    pages_fixture_file = os.path.join(APP_DIR, 'fixtures', 'pages.json')

    with open(pages_fixture_file) as page_fixture:
        data = json.load(page_fixture)

        return data


def get_dataset_data(filename):
    dataset_fixture_file = os.path.join(APP_DIR, 'fixtures', filename)

    with open(dataset_fixture_file) as dataset_fixture:
        data = dataset_fixture.read()

        return data
