from numpy import arange
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV


class RegressionModelOptimizer:
    @staticmethod
    def rf_regression_gs(X_train, y_train):
        """Search grid for random foresr regression"""

        parameters = {"n_estimators": [50, 500], "warm_start": ("True", "False")}

        rf = RandomForestRegressor(random_state=101, max_depth=10, max_leaf_nodes=20)
        gs_rf = GridSearchCV(rf, parameters, cv=5, iid=False)
        gs_rf.fit(X_train, y_train)

        hyperparameters_res = gs_rf.best_params_
        accuracy_gs = gs_rf.best_score_

        return hyperparameters_res, accuracy_gs

    @staticmethod
    def lss_regression_gs(X_train, y_train):
        """Search grid for Lasso regression"""

        a_range = list(arange(0.1, 1, 0.1))
        parameters = {"alpha": a_range, "normalize": ("True", "False")}

        lss = Lasso()
        gs_lss = GridSearchCV(lss, parameters, cv=5, iid=False)
        gs_lss.fit(X_train, y_train)

        hyperparameters_res = gs_lss.best_params_
        accuracy_gs = gs_lss.best_score_

        return hyperparameters_res, accuracy_gs

    @staticmethod
    def rg_regression_gs(X_train, y_train):
        """Search grid for Ridge regression"""

        a_range = list(arange(0.1, 1, 0.1))
        parameters = {"alpha": a_range}

        rg = Ridge(solver="auto")
        gs_rg = GridSearchCV(rg, parameters, cv=5, iid=False)
        gs_rg.fit(X_train, y_train)

        hyperparameters_res = gs_rg.best_params_
        accuracy_gs = gs_rg.best_score_

        return hyperparameters_res, accuracy_gs
