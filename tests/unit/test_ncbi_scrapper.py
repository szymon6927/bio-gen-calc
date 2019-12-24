from unittest.mock import patch

import pytest

from app.mail_scrapper.ncbi_scrapper import NCBIObject
from app.mail_scrapper.ncbi_scrapper import NCBIPubScrapper


@pytest.fixture
def example_search_response():
    return {
        'header': {'type': 'esearch', 'version': '0.3'},
        'esearchresult': {'count': '3638884', 'retmax': '2', 'retstart': '0', 'idlist': ['31782494', '31782426']},
    }


@pytest.fixture
def example_publication_content():
    return """name ml "Liu Z", affil str "Jan and Dan Duncan Neurological Research Institute,
        Texas Children's Hospital, Houston, TX, USA; Department of Pediatrics, Baylor
        College of Medicine, Houston, TX, USA; Quantitative and Computational
        Biosciences Program, Baylor College of Medicine, Houston, TX, USA. Electronic
        address: zhandong.liu@bcm.edu."""


@patch('app.mail_scrapper.ncbi_scrapper.requests.get')
def test_get_publication_id_list_ok(mock_get, example_search_response):
    mock_get.return_value.json.return_value = example_search_response
    mock_get.return_value.status_code = 200

    scrapper = NCBIPubScrapper()
    publication_list = scrapper.get_publication_id_list(0, 2)

    assert '31782494' in publication_list
    assert '31782426' in publication_list


@patch('app.mail_scrapper.ncbi_scrapper.requests.get')
def test_get_publication_id_list_wrong_status_code(mock_get):
    mock_get.return_value.status_code = 400

    scrapper = NCBIPubScrapper()
    publication_list = scrapper.get_publication_id_list(0, 2)

    assert publication_list == []


@patch('app.mail_scrapper.ncbi_scrapper.requests.get')
def test_get_publication_content_ok(mock_get, example_publication_content):
    mock_get.return_value.content.decode.return_value = example_publication_content
    mock_get.return_value.status_code = 200

    publication_id = '12345'

    scrapper = NCBIPubScrapper()
    publication_content = scrapper.get_publication_content(publication_id)

    assert 'Baylor College of Medicine' in publication_content


@patch('app.mail_scrapper.ncbi_scrapper.requests.get')
def test_get_publication_content_wrong_status_code(mock_get):
    mock_get.return_value.status_code = 400

    publication_id = '12345'

    scrapper = NCBIPubScrapper()
    publication_content = scrapper.get_publication_content(publication_id)

    assert publication_content is None


def test_get_extracted_emails_ok(example_publication_content):
    scrapper = NCBIPubScrapper()
    emails = scrapper.get_extracted_emails(example_publication_content)

    assert 'zhandong.liu@bcm.edu' in emails


def test_get_extracted_emails_multiple_mails():
    publication_content = """
    test test test
    test1@test.com
    another test string
    test2@test.com, lorem ipsum.
    test3@test.com
    """
    scrapper = NCBIPubScrapper()
    emails = scrapper.get_extracted_emails(publication_content)

    assert 'test1@test.com' in emails
    assert 'test2@test.com' in emails
    assert 'test3@test.com' in emails
    assert len(emails) == 3


def test_get_extracted_emails_no_mails():
    publication_content = """
    test test test
    another test string
    lorem ipsum.
    """
    scrapper = NCBIPubScrapper()
    emails = scrapper.get_extracted_emails(publication_content)

    assert len(emails) == 0


def test_create_ncbi_object():
    test_email = 'test@test.com'
    test_publication_id = '12345'

    test_ncbi_object = NCBIObject(
        email=test_email,
        publication_id=test_publication_id,
        publication_url=f'https://www.ncbi.nlm.nih.gov/pubmed/{test_publication_id}',
    )

    scrapper = NCBIPubScrapper()
    ncbi_object = scrapper.create_ncbi_object(test_email, test_publication_id)

    assert ncbi_object.email == test_ncbi_object.email
    assert ncbi_object.publication_id == test_ncbi_object.publication_id
    assert ncbi_object.publication_url == test_ncbi_object.publication_url
