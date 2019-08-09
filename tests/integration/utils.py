from werkzeug.security import generate_password_hash

from app.database import db
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
