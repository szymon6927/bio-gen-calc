import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.database import db
from app.userpanel.models import Customer
from app.userpanel.models import Page


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('testing')
    app.config.update(SQLALCHEMY_DATABASE_URI='sqlite://')

    with app.app_context():
        db.create_all()

        customers, pages = get_fixtures()
        for page in pages:
            db.session.add(page)

        db.session.commit()

        yield app

        db.drop_all()


@pytest.fixture
def test_client(app):
    """A test client for the app."""
    return app.test_client()


def get_fixtures():
    customers = [
        Customer(
            first_name="Test 1",
            last_name="Test 1",
            email="test1@test.com",
            login="test1",
            password=generate_password_hash("testing123", method='sha256'),
            is_superuser=True,
        ),
        Customer(
            first_name="Test 2",
            last_name="Test 2",
            email="test2@test.com",
            login="test2",
            password=generate_password_hash("testing321", method='sha256'),
        ),
    ]

    pages = [
        Page(name="Gene-Calc", is_active=1, slug="/", text="Test content text", desc="Test content desc"),
        Page(
            name="Materials & Methods",
            is_active=1,
            slug="/materials-and-methods",
            text="Test content text",
            desc="Test content desc",
        ),
        Page(
            name="Hardy-Weinberg equilibrium",
            is_active=1,
            slug="/hardy-weinber-page",
            text="Test content text",
            desc="Test content desc",
        ),
        Page(
            name="Chi-Square tests",
            is_active=1,
            slug="/chi-square-page",
            text="Test content text",
            desc="Test content desc",
        ),
        Page(
            name="Polymorphic information content & Heterozygosity",
            is_active=1,
            slug="/pic",
            text="Test content text",
            desc="Test content desc",
        ),
        Page(
            name="Genetic Distance",
            is_active=1,
            slug="/genetic-distance",
            text="Test content text",
            desc="Test content desc",
        ),
        Page(
            name="Dot plot",
            is_active=1,
            slug="/sequences-analysis-tools/dot-plot",
            text="Test content text",
            desc="Test content desc",
        ),
        Page(
            name="Consensus Sequence",
            is_active=1,
            slug="/sequences-analysis-tools/consensus-sequence",
            text="Test content text",
            desc="Test content desc",
        ),
        Page(
            name="Sequences Tools",
            is_active=1,
            slug="/sequences-analysis-tools/sequences-tools",
            text="Test content text",
            desc="Test content desc",
        ),
        Page(name="About", is_active=1, slug="/about", text="Test content text", desc="Test content desc"),
        Page(
            name="Our donors and cooperators",
            is_active=1,
            slug="/donors",
            text="Test content text",
            desc="Test content desc",
        ),
        Page(name="Contact Us", is_active=1, slug="/contact", text="Test content text", desc="Test content desc"),
        Page(
            name="Privacy policy",
            is_active=1,
            slug="/privacy-policy",
            text="Test content text",
            desc="Test content desc",
        ),
    ]

    return customers, pages
