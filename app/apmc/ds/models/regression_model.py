from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score


class RegressionModel:
    @staticmethod
    def linear_regression(**kwargs):
        """
        Linear regression model for regression problems
        Ordinary least squares
        """
        X_train = kwargs.get('X_train')
        y_train = kwargs.get('y_train')
        X_test = kwargs.get('X_test')

        lreg = LinearRegression()
        lreg.fit(X_train, y_train)
        predicted = lreg.predict(X_test)

        return lreg, predicted

    @staticmethod
    def lasso_regression(alpha=1.0, **kwargs):
        """Lasso regression model"""
        X_train = kwargs.get('X_train')
        y_train = kwargs.get('y_train')
        X_test = kwargs.get('X_test')

        lasso = Lasso(alpha=alpha)
        lasso.fit(X_train, y_train)
        predicted = lasso.predict(X_test)

        return lasso, predicted

    @staticmethod
    def ridge_regression(alpha=1.0, **kwargs):
        """Ridge regression model"""
        X_train = kwargs.get('X_train')
        y_train = kwargs.get('y_train')
        X_test = kwargs.get('X_test')

        ridge = Ridge(alpha=alpha)
        ridge.fit(X_train, y_train)
        predicted = ridge.predict(X_test)

        return ridge, predicted

    @staticmethod
    def random_forest_regression(random_state=101, n_estimators=100, **kwargs):
        """Random forest regressor model"""
        X_train = kwargs.get('X_train')
        y_train = kwargs.get('y_train')
        X_test = kwargs.get('X_test')

        rfr = RandomForestRegressor(random_state=random_state, n_estimators=n_estimators)
        rfr.fit(X_train, y_train)
        predicted = rfr.predict(X_test)

        return rfr, predicted

    @staticmethod
    def get_accuracy_score(y_test, predicted):
        return r2_score(y_test, predicted)
