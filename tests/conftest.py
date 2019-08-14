import pytest

from app import create_app
from app.database import db
from app.userpanel.models import Page
from tests.integration.utils import get_pages_fixture


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('testing')
    app.config.update(SQLALCHEMY_DATABASE_URI='sqlite://')

    with app.app_context():
        db.create_all()

        load_pages()

        yield app

        db.drop_all()


@pytest.fixture
def test_client(app):
    """A test client for the app."""
    return app.test_client()


def load_pages():
    pages_fixture = get_pages_fixture()

    for page_fixture in pages_fixture:
        page = Page(
            name=page_fixture.get('name'),
            is_active=page_fixture.get('is_active'),
            slug=page_fixture.get('slug'),
            text=page_fixture.get('text'),
            desc=page_fixture.get('desc'),
        )

        db.session.add(page)

    db.session.commit()
