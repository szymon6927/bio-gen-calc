import os

import requests
from flask import Blueprint
from flask import Response
from flask import abort
from flask import jsonify
from flask import request

from app.clients.slack_client import SlackNotification

slack_notification = SlackNotification()
newsletter = Blueprint('newsletter', __name__)


@newsletter.route('/newsletter/add', methods=['POST'])
def add_to_newsletter():
    """
    Add e-mail to newsletter list
    """
    data = request.get_json()
    email = data.get('email', None)

    if not email:
        return abort(Response("Provide email address", 400))

    slack_notification.added_to_newsletter(email)

    response, status_code = mailchimp_api_call(email)

    if status_code != 200:
        return abort(Response(response.get('title'), int(response.get('status'))))

    return jsonify({'status': '200', 'message': 'Thanks for adding to our newsletter.'})


def mailchimp_api_call(email):
    list_id = os.environ.get('MAILCHIMP_LIST_ID')
    api_key = os.environ.get('MAILCHIMP_API_KEY')
    mailchimp_username = os.environ.get('MAILCHIMP_USERNAME')

    api_url = f'https://us19.api.mailchimp.com/3.0/lists/{list_id}/members'
    headers = {'content-type': 'application/json'}
    data = {'email_address': email, 'status': "subscribed"}

    response = requests.post(api_url, auth=(mailchimp_username, api_key), headers=headers, json=data)
    return response.json(), response.status_code
