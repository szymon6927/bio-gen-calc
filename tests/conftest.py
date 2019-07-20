import pytest

from werkzeug.security import generate_password_hash

from app import create_app
from app.database import db
from app.models.Userpanel import Customer
from app.models.Admin import User, Page


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')
    flask_app.config.update(
        SQLALCHEMY_DATABASE_URI='sqlite://',
    )

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def init_db():
    db.create_all()

    customers, pages = create_db_rows()

    for customer in customers:
        db.session.add(customer)

    for page in pages:
        db.session.add(page)

    db.session.commit()

    yield db

    db.drop_all()


def create_db_rows():
    customers = [
        Customer(first_name="Test 1", last_name="Test 1", email="test1@test.com", login="test1",
                 password=generate_password_hash("testing123", method='sha256')),
        Customer(first_name="Test 2", last_name="Test 2", email="test2@test.com", login="test2",
                 password=generate_password_hash("testing321", method='sha256'))
    ]

    pages = [
        Page(name="Gene-Calc", is_active=1, breadcrumbs="/", text="Test content text", desc="Test content desc"),
        Page(name="Materials & Methods", is_active=1, breadcrumbs="/materials-and-methods", text="Test content text",
             desc="Test content desc"),
        Page(name="Hardy-Weinberg equilibrium", is_active=1, breadcrumbs="/hardy-weinber-page",
             text="Test content text", desc="Test content desc"),
        Page(name="Chi-Square tests", is_active=1, breadcrumbs="/chi-square-page", text="Test content text",
             desc="Test content desc"),
        Page(name="Polymorphic information content & Heterozygosity", is_active=1, breadcrumbs="/pic",
             text="Test content text", desc="Test content desc"),
        Page(name="Genetic Distance", is_active=1, breadcrumbs="/genetic-distance", text="Test content text",
             desc="Test content desc"),
        Page(name="Dot plot", is_active=1, breadcrumbs="/sequences-analysis-tools/dot-plot", text="Test content text",
             desc="Test content desc"),
        Page(name="Consensus Sequence", is_active=1, breadcrumbs="/sequences-analysis-tools/consensus-sequence",
             text="Test content text", desc="Test content desc"),
        Page(name="Sequences Tools", is_active=1, breadcrumbs="/sequences-analysis-tools/sequences-tools",
             text="Test content text", desc="Test content desc"),
        Page(name="About", is_active=1, breadcrumbs="/about", text="Test content text", desc="Test content desc"),
        Page(name="Our donors and cooperators", is_active=1, breadcrumbs="/donors", text="Test content text",
             desc="Test content desc"),
        Page(name="Contact Us", is_active=1, breadcrumbs="/contact", text="Test content text",
             desc="Test content desc"),
        Page(name="Privacy policy", is_active=1, breadcrumbs="/privacy-policy", text="Test content text",
             desc="Test content desc")
    ]

    return customers, pages
