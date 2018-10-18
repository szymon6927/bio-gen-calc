from ..database import db
import datetime


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
