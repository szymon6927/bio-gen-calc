import datetime

import numpy as np

from app.clients.slack_client import SlackNotification


def test_format_calculation_result():
    slack_notification = SlackNotification()

    example_calculation_result = [
        {'name': 'Foo 1', 'value': 'Bar 1'},
        {'name': 'Foo 2', 'value': 'Bar 2'},
        {'name': 'Foo 3', 'value': 'Bar 3'},
    ]

    expected_formatted_calculation_result = "Foo 1 = Bar 1\n" + "Foo 2 = Bar 2\n" + "Foo 3 = Bar 3\n"

    formatted_calculation_result = slack_notification._format_calculation_result(example_calculation_result)

    assert formatted_calculation_result == expected_formatted_calculation_result


def test_format_calculation_result_when_empty():
    slack_notification = SlackNotification()
    example_calculation_result = []

    formatted_calculation_result = slack_notification._format_calculation_result(example_calculation_result)

    assert formatted_calculation_result == ""


def test_format_user_input():
    slack_notification = SlackNotification()

    example_user_input = {'value_1': 1, 'value_2': 2, 'value_3': 3}

    expected_formatted_user_input = "value_1 = 1\n" + "value_2 = 2\n" + "value_3 = 3\n"

    formatted_user_input = slack_notification._format_user_input(example_user_input)

    assert formatted_user_input == expected_formatted_user_input


def test_test_format_user_input_when_empty():
    slack_notification = SlackNotification()

    example_user_input = dict()

    formatted_user_input = slack_notification._format_user_input(example_user_input)

    assert formatted_user_input == ""


def test_generic_notification_message():
    slack_notification = SlackNotification()

    module_name = "Test Module"

    example_user_input = {'value_1': 1, 'value_2': 2, 'value_3': 3}

    expected_formatted_user_input = "value_1 = 1\n" + "value_2 = 2\n" + "value_3 = 3\n"

    example_calculation_result = [
        {'name': 'Foo 1', 'value': 'Bar 1'},
        {'name': 'Foo 2', 'value': 'Bar 2'},
        {'name': 'Foo 3', 'value': 'Bar 3'},
    ]

    expected_formatted_calculation_result = "Foo 1 = Bar 1\n" + "Foo 2 = Bar 2\n" + "Foo 3 = Bar 3\n"

    ip_address = "127.0.0.1"
    dt_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    expected_msg = (
        f":bangbang: New calculation from *{module_name}* module :rocket:\n\n"
        + f":male-technologist: *User input:*\n"
        + f"```{expected_formatted_user_input}```\n\n"
        + ":rotating_light: *Calculation result:*\n"
        + f"```{expected_formatted_calculation_result}```\n\n"
        + f":globe_with_meridians: *IP Address:* `{ip_address}`\n"
        + f":date: *Date:* `{dt_now}`\n"
    )

    msg = slack_notification._generic_notification_message(
        module_name, example_user_input, example_calculation_result, ip_address
    )

    assert msg == expected_msg


def test_generic_notification_message_when_calculation_result_not_list():
    slack_notification = SlackNotification()

    module_name = "Test Module"

    example_user_input = {'value_1': 1, 'value_2': 2, 'value_3': 3}

    expected_formatted_user_input = "value_1 = 1\n" + "value_2 = 2\n" + "value_3 = 3\n"

    example_calculation_result = np.array([2, 3, 1, 0])

    ip_address = "127.0.0.1"
    dt_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    expected_msg = (
        f":bangbang: New calculation from *{module_name}* module :rocket:\n\n"
        + f":male-technologist: *User input:*\n"
        + f"```{expected_formatted_user_input}```\n\n"
        + ":rotating_light: *Calculation result:*\n"
        + f"```{example_calculation_result}```\n\n"
        + f":globe_with_meridians: *IP Address:* `{ip_address}`\n"
        + f":date: *Date:* `{dt_now}`\n"
    )

    msg = slack_notification._generic_notification_message(
        module_name, example_user_input, example_calculation_result, ip_address
    )

    assert msg == expected_msg
