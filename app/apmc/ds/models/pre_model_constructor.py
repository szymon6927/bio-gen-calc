import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.dummy import DummyRegressor
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_validate

from app.apmc.ds.common.enums import ModelTypeChoices
from app.apmc.ds.repositories.classification_model_repository import ClassificationModelRepository
from app.apmc.ds.repositories.regression_model_repository import RegressionModelRepository


class PreModelConstructor:
    """
    class with methods to: load and check data, select regression or classyfication model
    based off accuracy.

    path = data set file path with excel (xls or xlsx) or csv extension
    delimiter type = for instance ';' or ',' in case of csv files.
    model type = classification or regression
    """

    def __init__(self, model_type):
        self.model_type = model_type

    def _primary_model_evaluation_classification(self, Y_true, Y_predicted, cross_validate_score):
        accuracy = accuracy_score(Y_true, Y_predicted)
        matrix_report = classification_report(Y_true, Y_predicted, output_dict=True)
        df_matrix_report = pd.DataFrame(matrix_report)

        model_evaluation_metrics = {
            'matrix_report': df_matrix_report.to_html(),
            'cross_validate_score': cross_validate_score,
            'accuracy': accuracy,
        }

        return model_evaluation_metrics

    def _primary_model_evaluation_regression(self, Y_true, Y_predicted, cross_validate_score):
        mae = mean_absolute_error(Y_true, Y_predicted)
        mse = mean_squared_error(Y_true, Y_predicted)
        r2 = r2_score(Y_true, Y_predicted)

        model_evaluation_metrics = {'cross_validate_score': cross_validate_score, 'MAE': mae, 'MSE': mse, 'R2': r2}

        return model_evaluation_metrics

    def primary_model_evaluation(self, model, model_name, Y_true, Y_predicted, X_train, y_train):
        """method to basic evaluation of models collection
        model = instance of model
        model_name = name of algorithm
        Y_true = y_test values
        Y_predicted = y_values predicted by mentioned model
        """
        cross_validate_score = np.mean(cross_validate(model, X_train, y_train, cv=5)['test_score'])

        if self.model_type == ModelTypeChoices.classification:
            result = self._primary_model_evaluation_classification(Y_true, Y_predicted, cross_validate_score)
            result.update({'model_name': model_name})
            return result

        if self.model_type == ModelTypeChoices.regression:
            result = self._primary_model_evaluation_regression(Y_true, Y_predicted, cross_validate_score)
            result.update({'model_name': model_name})
            return result

        raise ValueError("No model type selected")

    def build_model_metrics(self, data):
        """
        Method to select accurate model for regression or classification problem based
        off accuracy and cross validation.
        Regression models: Random Forest and Linear Regression
        Classification models: KNN, Random Forest, Logistic Regression
        """
        X_train = data.get('X_train')
        y_train = data.get('y_train')
        y_test = data.get('y_test')

        all_models_metrics = list()

        repo_factory = {
            ModelTypeChoices.classification: ClassificationModelRepository(),
            ModelTypeChoices.regression: RegressionModelRepository(),
        }

        repo = repo_factory[self.model_type]

        for model_information in repo.get_repo():
            model_key, model_name, model_function, _ = model_information

            model_instance, predicted = model_function(**data)
            model_evaluation_metrics = self.primary_model_evaluation(
                model_instance, model_name, y_test, predicted, X_train, y_train
            )
            all_models_metrics.append(model_evaluation_metrics)

        return all_models_metrics, repo.get_user_choices()

    def dummy_comparison(self, models_metrics, y_train, X_train):
        """This method display warning for models which are less accurate than dummy equivalents"""
        warnings = []

        dummy_model_mapper = {
            ModelTypeChoices.classification: DummyClassifier(random_state=101),
            ModelTypeChoices.regression: DummyRegressor(),
        }

        dummy_model = dummy_model_mapper.get(self.model_type)

        threshold = np.mean(cross_validate(dummy_model, X_train, y_train, cv=5)['test_score'])

        for models_metric in models_metrics:
            accuracy = models_metric.get('cross_validate_score')
            model_name = models_metric.get('model_name')

            if accuracy < threshold:
                warnings.append(f"{model_name} in this step seems to be not acceptable to use")

        return warnings

    @staticmethod
    def get_best_model(models_metrics):

        """method to type best model for current problem from trained collection
        input is a dict with models accuracy scores [cross validation score]
        output is a model name with the best mean accuracy
        """
        best = max(models_metrics, key=lambda model: model['cross_validate_score'])
        return best['model_name']
