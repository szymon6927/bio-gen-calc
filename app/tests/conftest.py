import pytest
from .. import create_app


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
