import datetime

from app.database import db


class AMPCData(db.Model):
    __tablename__ = 'ampc_data'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    project_name = db.Column(db.String(120), nullable=False)
    dataset = db.Column(db.String(40), nullable=False)
    model_type = db.Column(db.String(120), nullable=False)
    normalization = db.Column(db.Boolean, default=False)
    trained_model = db.Column(db.String(40), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"AMPC data: {self.project_name}, {self.model_type}"
