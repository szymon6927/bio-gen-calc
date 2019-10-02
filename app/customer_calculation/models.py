import datetime

from app.database import db


class CustomerCalculation(db.Model):
    __tablename__ = 'customer_calculations'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(150), nullable=True)
    module_name = db.Column(db.String(120), nullable=True)
    customer_input = db.Column(db.Text, nullable=True)
    result = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return "<Customer Calculation: {} ({})>".format(self.module_name, self.created_at)
