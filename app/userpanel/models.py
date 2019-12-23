import datetime

from flask_login import UserMixin

from app import login_manager
from app.database import db


class Customer(UserMixin, db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    calculations = db.relationship('CustomerCalculation', backref='customer', passive_deletes=True)
    activity = db.relationship('CustomerActivity', backref='customer', passive_deletes=True)
    apmc_data = db.relationship('APMCData', backref='customer', lazy='joined')
    first_name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=True)
    profile_pic = db.Column(db.String(20), nullable=False, default='profile.svg')
    login = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(80))
    is_superuser = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return "<Customer: {} ({})>".format(self.first_name, self.last_name)


@login_manager.user_loader
def load_customer(obj_id):
    return Customer.query.get(int(obj_id))


class CustomerActivity(db.Model):
    __tablename__ = 'customer_activity'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'))
    module_name = db.Column(db.String(120), nullable=True)
    url = db.Column(db.String(120))


class Page(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    is_active = db.Column(db.Boolean(), default=True, unique=False)
    slug = db.Column(db.String(220))
    seo_title = db.Column(db.String(85))
    seo_desc = db.Column(db.String(180))
    seo_keywords = db.Column(db.String(200))
    text = db.Column(db.UnicodeText)
    desc = db.Column(db.UnicodeText)

    def __repr__(self):
        return self.name


class Calculation(db.Model):
    __tablename__ = 'calculations'

    id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(120))
    user_data = db.Column(db.Text)
    result = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return "<Calculation: {} ({})>".format(self.module_name, self.created_at)


class NCBIMailPackage(db.Model):
    __tablename__ = 'ncbi_mail_packages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.relationship('NCBIMail', backref='ncbi_mail_packages')
    was_sent = db.Column(db.Boolean, default=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"<NCBIMailPackage: {self.name}>"


class NCBIMail(db.Model):
    __tablename__ = 'ncbi_mails'

    id = db.Column(db.Integer, primary_key=True)
    publication_id = db.Column(db.String(50))
    ncbi_publication_url = db.Column(db.String(150))
    email = db.Column(db.String(100), unique=True)
    package_id = db.Column(db.Integer, db.ForeignKey('ncbi_mail_packages.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"<NCBIMail: {self.email}>"
