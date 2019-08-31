from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC


class ClassificationModel:
    @staticmethod
    def rf_classification(n_estimators=100, random_state=101, warm_start=False, **kwargs):
        """Random Forest Classifier"""
        X_train = kwargs.get('X_train')
        y_train = kwargs.get('y_train')
        X_test = kwargs.get('X_test')

        rfc = RandomForestClassifier(n_estimators=n_estimators, warm_start=warm_start, random_state=random_state)
        rfc.fit(X_train, y_train)
        predicted = rfc.predict(X_test)

        return rfc, predicted

    @staticmethod
    def knn_classification(n_neighbors=None, **kwargs):
        """K Neighbors Classifier"""
        X_train = kwargs.get('X_train')
        y_train = kwargs.get('y_train')
        X_test = kwargs.get('X_test')
        y_test = kwargs.get('y_test')

        if not n_neighbors:
            dict_of_results = {}  # for k-n model

            for k in range(1, 10):
                if k % 2 != 0:
                    knn = KNeighborsClassifier(n_neighbors=k)
                    knn.fit(X_train, y_train)
                    predicted = knn.predict(X_test)
                    accuracy = accuracy_score(y_test, predicted)
                    dict_of_results.update({k: accuracy})

            best_k = max(dict_of_results, key=dict_of_results.get)
            knn = KNeighborsClassifier(n_neighbors=best_k)
            knn.fit(X_train, y_train)
            predicted = knn.predict(X_test)
        else:
            knn = KNeighborsClassifier(n_neighbors=n_neighbors)
            knn.fit(X_train, y_train)
            predicted = knn.predict(X_test)

        return knn, predicted

    @staticmethod
    def lr_classification(max_iter=50000, C=1, solver="saga", warm_start=True, multi_class="auto", **kwargs):
        """Logistic Regression Classifier"""
        X_train = kwargs.get('X_train')
        y_train = kwargs.get('y_train')
        X_test = kwargs.get('X_test')

        lr = LogisticRegression(solver=solver, max_iter=max_iter, C=C, warm_start=warm_start, multi_class=multi_class)

        lr.fit(X_train, y_train)
        predicted = lr.predict(X_test)

        return lr, predicted

    @staticmethod
    def svm_classification(C=1.0, gamma="auto", kernel="rbf", degree=3, **kwargs):
        """Supported vector machines classification"""
        X_train = kwargs.get('X_train')
        y_train = kwargs.get('y_train')
        X_test = kwargs.get('X_test')

        svm_model = SVC(C=C, gamma=gamma, kernel=kernel, degree=degree)
        svm_model.fit(X_train, y_train)
        predicted = svm_model.predict(X_test)

        return svm_model, predicted

    @staticmethod
    def get_accuracy_score(y_test, predicted):
        return accuracy_score(y_test, predicted)
