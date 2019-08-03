from werkzeug.security import generate_password_hash

from app.database import db
from app.userpanel.models import Customer


def test_valid_login_logout(test_client):
    print("test_client: ", test_client)
    data = {"login_or_email": "test123@test.com", "password": "testing123"}

    customer = Customer(
        first_name="Test 3",
        last_name="Test 3",
        email="test123@test.com",
        login="test123",
        password=generate_password_hash("testing123", method='sha256'),
        is_superuser=True,
    )
    db.session.add(customer)
    db.session.commit()

    all_customers = Customer.query.all()
    print("all_customers: ", all_customers)

    response = test_client.post('/userpanel/login', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b"Invalid username or password" not in response.data
    assert b"Welcome" in response.data


def test_invalid_login_logout(test_client):
    data = {"login_or_email": "test2@test.com", "password": "testing321321"}

    response = test_client.post('/userpanel/login', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b"Invalid username or password" in response.data
