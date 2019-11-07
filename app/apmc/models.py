import datetime
import json
import os

from flask import current_app

from app.apmc.config import APMC_DATASET_UPLOAD_PATH
from app.apmc.config import APMC_MODELS_UPLOAD_PATH
from app.apmc.ds.common.constants import RANDOM_FOREST_NAMES
from app.database import db


class APMCData(db.Model):
    __tablename__ = 'apmc_data'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    project_name = db.Column(db.String(120), nullable=False)
    dataset = db.Column(db.String(80), nullable=False)
    model_type = db.Column(db.String(120), nullable=False)
    normalization = db.Column(db.Boolean, default=False)
    trained_model = db.Column(db.String(40), nullable=True)
    training_completed = db.Column(db.Boolean, default=False)
    model_metrics = db.Column(db.Text, nullable=True)
    report = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def dataset_path(self):
        return os.path.join(current_app.root_path, APMC_DATASET_UPLOAD_PATH, self.dataset)

    def model_path(self):
        if self.trained_model:
            return os.path.join(current_app.root_path, APMC_MODELS_UPLOAD_PATH, self.trained_model)

        return None

    @property
    def model_name(self):
        if self.model_metrics:
            model_metrics = json.loads(self.model_metrics)
            return model_metrics.get('model_name', None)

        return None

    @property
    def has_tree_graph(self):
        return self.model_name in RANDOM_FOREST_NAMES

    def __repr__(self):
        return f"APMC data: {self.project_name}, {self.model_type}"
