import numpy as np

from app.ampc.ds.common.enums import ModelTypeChoices


class Validator:
    def __init__(self, X, y, model_type):
        self.X_array = X
        self.y_vector = y
        self.model_type = model_type

    def _shape_validation(self):
        """Method to check in-data shape"""

        X_shape = self.X_array.shape
        y_shape = self.y_vector.shape

        if X_shape[1] > 10:
            raise ValueError("More then allowed predictors !")

        if y_shape[0] > 10000:
            raise ValueError("More then allowed records !")

    def _data_NaN(self):
        """Method to find NaN"""

        if np.isnan(self.X_array).any():
            raise ValueError("NaN in X_array data !")

        if self.model_type == ModelTypeChoices.regression and np.isnan(self.y_vector).any():
            raise ValueError("NaN in y_vector data !")

    def _data_quality(self):
        """Method to find string in input data. In case of X_array strings are not allowed,
        in case of categrocial models in y_vector strings are allowed"""

        try:
            self.X_array.astype(float)
        except ValueError:
            raise ValueError(
                "Data in X_array must be numerical, If data is categorical convert alphabetic "
                "labels to corresponding numbers"
            )  # TODO: custom exception

        if self.model_type == ModelTypeChoices.regression:
            try:
                self.y_vector.astype(float)
            except ValueError:
                raise ValueError("Data in y_vector must be numerical")  # TODO: custom exception

    def validate(self):
        self._shape_validation()
        self._data_quality()
        self._data_NaN()

        return True
