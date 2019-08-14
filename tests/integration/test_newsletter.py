import json
from unittest.mock import patch

from tests.integration.constants import URL


@patch('app.newsletter.views.mailchimp_api_call')
def test_post_newsletter_ok(mailchimp_mock, test_client):
    mailchimp_mock.return_value = {'status': "subscribed", 'message': "User added!"}, 200

    data = {'email': "test@test.com"}

    response = test_client.post(URL.NEWSLETTER_POST, data=json.dumps(data), content_type='application/json')
    result = json.loads(response.data)

    assert response.status_code == 200
    assert result['message'] == "Thanks for adding to our newsletter."


def test_post_newsletter_when_email_not_provided(test_client):
    data = {'email': ""}

    response = test_client.post(URL.NEWSLETTER_POST, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    assert b'Provide email address' in response.data


@patch('app.newsletter.views.mailchimp_api_call')
def test_post_newsletter_invalid_email(mailchimp_mock, test_client):
    mailchimp_mock.return_value = {'title': "Invalid email", 'status': "400"}, 400

    data = {'email': "test@test"}

    response = test_client.post(URL.NEWSLETTER_POST, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    assert b'Invalid email' in response.data
