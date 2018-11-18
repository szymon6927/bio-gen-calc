from flask_login import UserMixin
from ..database import db
import datetime


class Customer(UserMixin, db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    calculations = db.relationship('CustomerCalculation', backref='customer', lazy='joined')
    activity = db.relationship('CustomerActivity', backref='customer', lazy='joined')
    first_name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=True)
    profile_pic = db.Column(db.String(20), nullable=False, default='profile.svg')
    login = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return "<Customer: {} ({})>".format(self.first_name, self.last_name)


class CustomerCalculation(db.Model):
    __tablename__ = 'customer_calculations'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    title = db.Column(db.String(150), nullable=True)
    module_name = db.Column(db.String(120), nullable=True)
    customer_input = db.Column(db.Text, nullable=True)
    result = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return "<Customer Calculation: {} ({})>".format(self.module_name, self.created_at)


class CustomerActivity(db.Model):
    __tablename__ = 'customer_activity'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    module_name = db.Column(db.String(120), nullable=True)
    url = db.Column(db.String(120))