import numpy as np
import pandas as pd

from app.apmc.ds.common.enums import ModelTypeChoices
from app.apmc.exceptions import DatasetValidationError


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
            raise DatasetValidationError("More then allowed predictors !")

        if y_shape[0] > 10000:
            raise DatasetValidationError("More then allowed records !")

    def _model_type_test(self):
        """Only strings allowed as target value in case of classification models!"""

        def is_number(char):
            if isinstance(char, int) or isinstance(char, float):
                raise DatasetValidationError(
                    "In classification models numbers are not allowed as target values, "
                    "convert number to the corresponding labels"
                )

        if self.model_type == ModelTypeChoices.classification:
            y_list = self.y_vector.tolist()

            for y in y_list:
                is_number(y)

    def _data_NaN(self):
        """Method to find NaN"""

        if np.isnan(self.X_array).any():
            raise DatasetValidationError("NaN in predictors data !")
        
        y_vector = pd.Series(self.y_vector)

        if pd.isnull(y_vector).any():
            raise DatasetValidationError("NaN in target value data !")

    def _number_target_class(self):
        unique_items = set(self.y_vector.tolist())

        if len(unique_items) < 2:
            raise DatasetValidationError(f"{unique_items} -> Less than allowed number of classes in target value")

    def _data_quality(self):
        """Method to find string in input data. In case of X_array strings are not allowed,
        in case of categrocial models in y_vector strings are allowed"""

        try:
            self.X_array.astype(float)
        except ValueError:
            raise DatasetValidationError(
                "Predictors must be numerical, If data is categorical convert alphabetic "
                "labels to corresponding numbers"
            )

        if self.model_type == ModelTypeChoices.regression:
            try:
                self.y_vector.astype(float)

            except ValueError:
                raise DatasetValidationError("Target data must be numerical in case of regression models")

    def validate(self):
        self._shape_validation()
        self._data_quality()
        self._data_NaN()
        self._number_target_class()
        self._model_type_test()

        return True
