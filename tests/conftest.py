import pytest

from app import create_app
from app.database import db
from app.userpanel.models import NCBIMail
from app.userpanel.models import NCBIMailPackage
from app.userpanel.models import Page
from tests.integration.utils import get_fixture


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('testing')
    app.config.update(SQLALCHEMY_DATABASE_URI='sqlite://')

    with app.app_context():
        db.create_all()

        load_pages()
        load_ncbi_packages()
        load_ncbi_mails()

        yield app

        db.drop_all()


@pytest.fixture
def test_client(app):
    """A test client for the app."""
    return app.test_client()


def load_pages():
    pages_fixture = get_fixture('pages.json')

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


def load_ncbi_packages():
    packages_fixture = get_fixture('ncbi_mail_packages.json')

    for package_fixture in packages_fixture:
        ncbi_package = NCBIMailPackage(
            name=package_fixture.get('name'),
            was_sent=package_fixture.get('was_sent'),
            comment=package_fixture.get('comment'),
        )

        db.session.add(ncbi_package)

    db.session.commit()


def load_ncbi_mails():
    mails_fixture = get_fixture('ncbi_mails.json')

    for mail_fixture in mails_fixture:
        ncbi_mail = NCBIMail(
            publication_id=mail_fixture.get('publication_id'),
            ncbi_publication_url=mail_fixture.get('ncbi_publication_url'),
            email=mail_fixture.get('email'),
            package_id=mail_fixture.get('package_id'),
        )

        db.session.add(ncbi_mail)

    db.session.commit()
