from app.ampc.ds.models.classification_model import ClassificationModel
from app.ampc.ds.models.classification_model_optimizer import ClassificationModelOptimizer


class ModelName:
    """Class which contain key, name tuples"""

    rf = ('rnn', "Random forest classification")
    knn = ('knn', "KNN classification")
    lr = ('lr', "Logistic regression")
    svmc = ('svmc', "Supported vector machines classification")


class ClassificationModelRepository:
    REPOSITORY = [
        (*ModelName.rf, ClassificationModel.rf_classification, ClassificationModelOptimizer.lr_classification_gs),
        (*ModelName.knn, ClassificationModel.knn_classification, ClassificationModelOptimizer.knn_classification_gs),
        (*ModelName.lr, ClassificationModel.lr_classification, ClassificationModelOptimizer.lr_classification_gs),
        (*ModelName.svmc, ClassificationModel.svm_classification, ClassificationModelOptimizer.svm_classification_gs),
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
