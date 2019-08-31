from app.ampc.ds.models.regression_model import RegressionModel
from app.ampc.ds.models.regression_model_optimizer import RegressionModelOptimizer


class ModelName:
    """Class which contain key, name tuples"""

    slr = ('slr', "Simple linear regression")
    llr = ('llr', "Lasso linear regression")
    rlr = ('rlr', "Ridge linear regression")
    rfr = ('rfr', "Random forest regression")


class RegressionModelRepository:
    REPOSITORY = [
        (*ModelName.slr, RegressionModel.linear_regression, None),
        (*ModelName.llr, RegressionModel.lasso_regression, RegressionModelOptimizer.lss_regression_gs),
        (*ModelName.rlr, RegressionModel.ridge_regression, RegressionModelOptimizer.rg_regression_gs),
        (*ModelName.rfr, RegressionModel.random_forest_regression, RegressionModelOptimizer.rf_regression_gs),
    ]

    def get_repo(self):
        return self.REPOSITORY

    def get_user_choices(self):
        """Get key, name model list which will be displayed as user choices"""
        user_choices = []

        for model in self.REPOSITORY:
            model_key, model_name, _, _ = model

            user_choices.append({'key': model_key, 'name': model_name})

        return user_choices

    def get_function(self, wanted_model_key):
        for model in self.REPOSITORY:
            model_key, _, function, _ = model

            if wanted_model_key == model_key:
                return function

    def get_optimizer(self, wanted_model_key):
        for model in self.REPOSITORY:
            model_key, _, _, optimize_function = model

            if wanted_model_key == model_key:
                return optimize_function
