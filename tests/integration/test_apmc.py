import json
from io import BytesIO
from unittest.mock import patch

from app.apmc.models import APMCData
from tests.integration.constants import URL
from tests.integration.utils import create_customer
from tests.integration.utils import get_dataset_data
from tests.integration.utils import login_customer


def test_get_apmc_ok(test_client):
    response = test_client.get(URL.APMC_GET)

    assert response.status_code == 200
    assert b'APMC' in response.data


def test_get_apmc_as_not_logged_in_user(test_client):
    response = test_client.get(URL.APMC_GET)

    assert response.status_code == 200
    assert b'You have to be logged in' in response.data


def test_get_apmc_as_logged_in_user(test_client):
    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    response = test_client.get(URL.APMC_GET)

    assert response.status_code == 200
    assert b'Your project name' in response.data
    assert b'Click to upload file' in response.data
    assert b'Pre-train' in response.data


def test_get_apmc_how_to_use_ok(test_client):
    response = test_client.get(URL.APMC_HOW_TO_USE_GET)

    assert response.status_code == 200
    assert b'How to use' in response.data


def test_get_apmc_documentation_ok(test_client):
    response = test_client.get(URL.APMC_DOCUMENTATION_GET)

    assert response.status_code == 200
    assert b'Documentation' in response.data


def test_post_apmc_pre_train_when_user_not_logged_in(test_client):
    data = dict()
    data['project_name'] = "Test project name"

    file_content = """FILE CONTENT"""
    data['file'] = (BytesIO(file_content.encode()), 'test_dataset.csv')
    data['model_type'] = "classification"
    data['normalization'] = False

    response = test_client.post(
        URL.APMC_PRE_TRAIN_POST, data=data, content_type='multipart/form-data', follow_redirects=True
    )

    assert response.status_code == 200
    assert b'Login to your account' in response.data


@patch('app.apmc.views.secrets')
def test_post_apmc_pre_train_classification_ok(secrets_mock, test_client):
    secrets_mock.token_hex.return_value = 100

    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    data = dict()
    data['project_name'] = "Test project name"
    file_content = get_dataset_data('iris_dataset.csv')
    data['file'] = (BytesIO(file_content.encode()), 'apmc_test_dataset.csv')
    data['model_type'] = "classification"
    data['normalization'] = False

    response = test_client.post(URL.APMC_PRE_TRAIN_POST, data=data, content_type='multipart/form-data')
    pre_train_result = json.loads(response.data)

    assert response.status_code == 200
    assert 'data_id' in pre_train_result
    assert 'model_metrics' in pre_train_result
    assert 'user_choices' in pre_train_result
    assert 'best_model' in pre_train_result
    assert 'dummy_model_warnings' in pre_train_result


@patch('app.apmc.views.secrets')
def test_post_apmc_pre_train_regression_ok(secrets_mock, test_client):
    secrets_mock.token_hex.return_value = 100

    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    data = dict()
    data['project_name'] = "Test project name"
    file_content = get_dataset_data('usa_dataset.csv')
    data['file'] = (BytesIO(file_content.encode()), 'apmc_test_dataset.csv')
    data['model_type'] = "regression"
    data['normalization'] = False

    response = test_client.post(URL.APMC_PRE_TRAIN_POST, data=data, content_type='multipart/form-data')
    pre_train_result = json.loads(response.data)

    assert response.status_code == 200
    assert 'data_id' in pre_train_result
    assert 'model_metrics' in pre_train_result
    assert 'user_choices' in pre_train_result
    assert 'best_model' in pre_train_result
    assert 'dummy_model_warnings' in pre_train_result


@patch('app.apmc.views.secrets')
def test_post_apmc_train_classification_ok(secrets_mock, test_client):
    secrets_mock.token_hex.return_value = 100

    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    pre_train_data = dict()
    pre_train_data['project_name'] = "Test project name"
    file_content = get_dataset_data('iris_dataset.csv')
    pre_train_data['file'] = (BytesIO(file_content.encode()), 'apmc_test_dataset.csv')
    pre_train_data['model_type'] = "classification"
    pre_train_data['normalization'] = False

    test_client.post(URL.APMC_PRE_TRAIN_POST, data=pre_train_data, content_type='multipart/form-data')

    apmc_data = APMCData.query.first()

    train_data = dict()
    train_data['data_id'] = apmc_data.id
    train_data['selected_model'] = "lr"

    response = test_client.post(URL.APMC_TRAIN_POST, data=json.dumps(train_data), content_type='application/json')

    assert response.status_code == 200


@patch('app.apmc.views.secrets')
def test_post_apmc_train_regression_ok(secrets_mock, test_client):
    secrets_mock.token_hex.return_value = 100

    customer, plain_password = create_customer()
    login_customer(test_client, customer.login, plain_password)

    pre_train_data = dict()
    pre_train_data['project_name'] = "Test project name"
    file_content = get_dataset_data('usa_dataset.csv')
    pre_train_data['file'] = (BytesIO(file_content.encode()), 'apmc_test_dataset.csv')
    pre_train_data['model_type'] = "regression"
    pre_train_data['normalization'] = False

    test_client.post(URL.APMC_PRE_TRAIN_POST, data=pre_train_data, content_type='multipart/form-data')

    apmc_data = APMCData.query.first()

    train_data = dict()
    train_data['data_id'] = apmc_data.id
    train_data['selected_model'] = "llr"

    response = test_client.post(URL.APMC_TRAIN_POST, data=json.dumps(train_data), content_type='application/json')

    assert response.status_code == 200
