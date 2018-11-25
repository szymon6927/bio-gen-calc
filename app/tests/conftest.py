import pytest
from .. import create_app
from ..database import db
from ..models.Userpanel import Customer
from ..models.Admin import User


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')
    flask_app.config.update(
        SQLALCHEMY_DATABASE_URI='sqlite://'
    )

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def init_db():
    db.create_all()

    customer = Customer(first_name="Test", last_name="Test", email="test@test.com", login="test", password="testing123")
    db.session.add(customer)

    db.session.commit()

    yield db

    db.drop_all()
