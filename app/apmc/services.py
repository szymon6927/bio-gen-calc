from app.apmc.ds.common.enums import ModelTypeChoices
from app.apmc.ds.common.validation import Validator
from app.apmc.ds.models.model import Model
from app.apmc.ds.models.pre_model_constructor import PreModelConstructor
from app.apmc.ds.processing.data_processing import data_set_split
from app.apmc.ds.processing.data_processing import load_data
from app.apmc.ds.repositories.classification_model_repository import ClassificationModelRepository
from app.apmc.ds.repositories.regression_model_repository import RegressionModelRepository
from app.apmc.models import AMPCData
from app.database import db


def pre_train(apmc_data: AMPCData) -> dict:
    pre_model_creator = PreModelConstructor(model_type=apmc_data.model_type)

    loaded_data = load_data(apmc_data.dataset_path())
    X_array = loaded_data.get('X_array')
    y_vector = loaded_data.get('y_vector')

    validation = Validator(X=X_array, y=y_vector, model_type=apmc_data.model_type)
    validation.validate()

    split_data = data_set_split(X_array, y_vector, normalization=apmc_data.normalization)

    model_metrics, user_choices = pre_model_creator.build_model_metrics(split_data)

    return {
        'model_metrics': model_metrics,
        'user_choices': user_choices,
        'best_model': PreModelConstructor.get_best_model(model_metrics),
    }


def train(apmc_data_id, selected_model):
    apmc_data = AMPCData.query.get_or_404(apmc_data_id)

    repo_factory = {
        ModelTypeChoices.classification: ClassificationModelRepository(),
        ModelTypeChoices.regression: RegressionModelRepository(),
    }
    repo = repo_factory[apmc_data.model_type]

    loaded_data = load_data(apmc_data.dataset_path())
    X_array = loaded_data.get('X_array')
    y_vector = loaded_data.get('y_vector')

    split_data = data_set_split(X_array, y_vector, normalization=apmc_data.normalization)

    X_train = split_data.get('X_train')
    y_train = split_data.get('y_train')

    model_function = repo.get_function(selected_model)
    optimizer = repo.get_optimizer(selected_model)

    if optimizer:
        hyperparameters, accuracy_gs = optimizer(X_train, y_train)
        model, _ = model_function(**hyperparameters, **split_data)
    else:
        model, _ = model_function(**split_data)

    model_path = Model.export_model(apmc_data_id, selected_model, apmc_data.model_type, model)

    apmc_data.trained_model = model_path
    db.session.add(apmc_data)
    db.session.commit()

    return model_path