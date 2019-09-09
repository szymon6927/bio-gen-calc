import json

from app.apmc.ds.common.enums import ModelTypeChoices
from app.apmc.ds.common.validation import Validator
from app.apmc.ds.models.model import Model
from app.apmc.ds.models.pre_model_constructor import PreModelConstructor
from app.apmc.ds.processing.data_processing import data_set_split
from app.apmc.ds.processing.data_processing import load_data
from app.apmc.ds.report.report_generator import ReportGenerator
from app.apmc.ds.repositories.classification_model_repository import ClassificationModelRepository
from app.apmc.ds.repositories.regression_model_repository import RegressionModelRepository
from app.apmc.models import APMCData
from app.database import db


def pre_train(apmc_data: APMCData) -> dict:
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
    apmc_data: APMCData = APMCData.query.get_or_404(apmc_data_id)

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
    Y_true = split_data.get('y_test')

    model_function = repo.get_function(selected_model)
    optimizer = repo.get_optimizer(selected_model)
    model_name = repo.get_model_name(selected_model)

    if optimizer:
        hyperparameters, accuracy_gs = optimizer(X_train, y_train)
        model, predicted = model_function(**hyperparameters, **split_data)
    else:
        model, predicted = model_function(**split_data)

    pre_model_constructor = PreModelConstructor(model_type=apmc_data.model_type)
    model_metrics = pre_model_constructor.primary_model_evaluation(
        model, model_name, Y_true, predicted, X_train, y_train
    )

    model_path = Model.export_model(apmc_data_id, selected_model, apmc_data.model_type, model)

    apmc_data.trained_model = model_path
    apmc_data.training_completed = True
    apmc_data.model_metrics = json.dumps(model_metrics)

    db.session.add(apmc_data)
    db.session.commit()

    generate_report(apmc_data_id)

    return model_path


def generate_report(apmc_data_id):
    apmc_data: APMCData = APMCData.query.get_or_404(apmc_data_id)

    report_generator = ReportGenerator(apmc_data)
    report_filename = report_generator.generate_report()

    apmc_data.report = report_filename

    db.session.add(apmc_data)
    db.session.commit()
