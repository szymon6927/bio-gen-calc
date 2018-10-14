from flask import request, jsonify
from . import newsletter
import requests
import os


@newsletter.route('/newsletter/add', methods=['POST'])
def add_to_newsletter():
    """
    Add e-mail to newsletter list
    """
    data = request.get_json()
    email = data.get('email', None)
    if email is not None:
        response, status_code = mailchimp_api_call(email)
        if status_code == 200:
            return jsonify({'status': '200', 'message': 'Thanks for adding to our newsletter.'})
        else:
            return response.get('title'), int(response.get('status'))


def mailchimp_api_call(email):
    list_id = os.environ.get('MAILCHIMP_LIST_ID')
    api_key = os.environ.get('MAILCHIMP_API_KEY')

    api_url = f'https://us19.api.mailchimp.com/3.0/lists/{list_id}/members'
    headers = {'content-type': 'application/json'}
    data = {
        "email_address": email,
        "status": "subscribed"
    }
    response = requests.post(api_url, auth=('szymon6927', api_key), headers=headers, json=data)
    return response.json(), response.status_code

