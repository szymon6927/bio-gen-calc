from numpy import arange
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC


class ClassificationModelOptimizer:
    @staticmethod
    def rf_classification_gs(X_train, y_train):
        """Search grid for randof forest classification"""
        parameters = {"n_estimators": [50, 500], "warm_start": ("True", "False")}

        rfc = RandomForestClassifier(random_state=101)
        gs_rfc = GridSearchCV(rfc, parameters, cv=5, iid=False)
        gs_rfc.fit(X_train, y_train)

        hyperparameters_res = gs_rfc.best_params_
        accuracy_gs = gs_rfc.best_score_

        return hyperparameters_res, accuracy_gs

    @staticmethod
    def knn_classification_gs(X_train, y_train):
        """Search grid for KNN classification"""

        def odd(x):
            if x % 2 != 0:
                return x

        k_values = list(filter(odd, range(50)))

        parameters = {
            "n_neighbors": k_values,
            "weights": ("uniform", "distance"),
            "algorithm": ("ball_tree", "kd_tree", "brute"),
            "p": [1, 2],
        }

        knn = KNeighborsClassifier()
        gs_knn = GridSearchCV(knn, parameters, cv=5, iid=False)
        gs_knn.fit(X_train, y_train)

        hyperparameters_res = gs_knn.best_params_
        accuracy_gs = gs_knn.best_score_

        return hyperparameters_res, accuracy_gs

    @staticmethod
    def lr_classification_gs(X_train, y_train):
        """Search grid for logistic regression classification"""

        c_range = list(arange(0.1, 1, 0.1))
        parameters = {"warm_start": ("True", "False"), "C": c_range}

        lr = LogisticRegression(multi_class="auto", solver="lbfgs", max_iter=5000)
        gs_lr = GridSearchCV(lr, parameters, cv=5, iid=False)
        gs_lr.fit(X_train, y_train)

        hyperparameters_res = gs_lr.best_params_
        accuracy_gs = gs_lr.best_score_

        return hyperparameters_res, accuracy_gs

    @staticmethod
    def svm_classification_gs(X_train, y_train):
        """Grid Search for supported vector machines model"""

        c_range = list(arange(0.1, 1, 0.1))
        degree_range = range(1, 10)

        parameters = {"C": c_range, "kernel": ("linear", "poly", "rbf", "sigmoid"), "degree": degree_range}
        svm_model = SVC(gamma="auto")

        gs_svm = GridSearchCV(svm_model, parameters, cv=5, iid=False)
        gs_svm.fit(X_train, y_train)

        hyperparameters_res = gs_svm.best_params_
        accuracy_gs = gs_svm.best_score_

        return hyperparameters_res, accuracy_gs
