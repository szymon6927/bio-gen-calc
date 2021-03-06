from unittest.mock import patch

from app.clients.slack_client import SlackClient


@patch('app.clients.slack_client.requests.post')
def test_send_message(requests_posts_mock):
    requests_posts_mock.return_value.ok = True
    requests_posts_mock.return_value.content = "ok"

    slack_client = SlackClient()
    slack_client.webhook_url = "https://hooks.slack.com/services/test-webhook"
    response = slack_client.send_message("test slack msg")

    assert response is not None
    assert response == "ok"


def test_send_message_when_no_webhook():
    slack_client = SlackClient()
    response = slack_client.send_message("test slack msg")

    assert response is None


@patch('app.clients.slack_client.requests.post')
def test_send_message_without_msg(requests_posts_mock):
    requests_posts_mock.return_value.ok = False

    slack_client = SlackClient()
    response = slack_client.send_message("")

    assert response is None
