import json
from typing import List

import joblib
import numpy as np

from app.apmc.ds.processing.data_processing import data_set_split
from app.apmc.ds.processing.data_processing import extrapolation_risk
from app.apmc.ds.processing.data_processing import load_data
from app.apmc.models import APMCData


class APMCUserPanelService:
    def __init__(self, apmc_data: APMCData):
        self.apmc_data = apmc_data
        self.user_input = None
        self.loaded_data = load_data(apmc_data.dataset_path())
        self.split_data = data_set_split(
            self.loaded_data.get('X_array'), self.loaded_data.get('y_vector'), normalization=apmc_data.normalization
        )

    def set_user_input(self, input_values: List):
        if self.apmc_data.normalization:
            scaled_values = []
            mean_array = self.split_data.get('X_mean')
            std_array = self.split_data.get('X_std')

            for counter, input_value in enumerate(input_values):
                input_value = float(input_value)

                try:
                    scaled_input_value = (input_value - mean_array[counter]) / std_array[counter]
                except ZeroDivisionError:
                    raise

                scaled_values.append(scaled_input_value)

            self.user_input = np.array(scaled_values).reshape(1, -1).astype(np.float64)
        else:
            self.user_input = np.array(input_values).reshape(1, -1).astype(np.float64)

    def get_user_input(self):
        return self.user_input

    def get_X_names(self):
        return self.loaded_data.get('X_names').tolist()

    def get_extrapolation_risk(self):
        return extrapolation_risk(self.split_data.get('X_train'), self.user_input, self.loaded_data.get('X_names'))

    def get_predicted_data(self):
        model = joblib.load(self.apmc_data.model_path())
        predicted_data = model.predict(self.user_input)

        return predicted_data.tolist()

    def get_model_metric(self):
        model_evaluation_metrics = json.loads(self.apmc_data.model_metrics)

        return model_evaluation_metrics
