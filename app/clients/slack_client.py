import datetime
import json
import os
from typing import Dict
from typing import List
from typing import Union

import numpy as np
import requests

from app.apmc.models import APMCData
from app.common.constants import ModuleName
from app.userpanel.models import Customer

CALCULATION_TYPE = Union[List[Dict], np.ndarray]


class SlackClient:
    def __init__(self):
        self.webhook_url = os.environ.get('SLACK_WEBHOOK_URL')

    def send_message(self, msg):
        headers = {'Content-type': 'application/json'}
        data = {'text': msg}

        response = requests.post(self.webhook_url, headers=headers, data=json.dumps(data))

        return response


class SlackNotification:
    def __init__(self):
        self.client = SlackClient()

    def _format_calculation_result(self, calculation_result: List[Dict]):
        formatted_calculation_result = ''

        for item in calculation_result:
            name = item.get('name')
            value = item.get('value')
            formatted_calculation_result += f'{name} = {value}\n'

        return formatted_calculation_result

    def _format_user_input(self, user_input: dict):
        formatted_user_input = ''
        for key, value in user_input.items():
            formatted_user_input += f'{key} = {value}\n'

        return formatted_user_input

    def _generic_notification_message(
        self, module_name: str, user_input: dict, calculation_result: CALCULATION_TYPE, ip_address: str
    ):

        if isinstance(calculation_result, list):
            calculation_result = self._format_calculation_result(calculation_result)

        dt_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        msg = (
            f":bangbang: New calculation from *{module_name}* module :rocket:\n\n"
            + f":male-technologist: *User input:*\n"
            + f"```{self._format_user_input(user_input)}```\n\n"
            + ":rotating_light: *Calculation result:*\n"
            + f"```{calculation_result}```\n\n"
            + f":globe_with_meridians: *IP Address:* `{ip_address}`\n"
            + f":date: *Date:* `{dt_now}`\n"
        )

        return msg

    def hardy_weinberg_calculation(self, user_input: dict, calculation_result: List[Dict], ip_address: str):
        msg = self._generic_notification_message(ModuleName.HARDY_WEINBERG, user_input, calculation_result, ip_address)
        res = self.client.send_message(msg)
        return res

    def pic_codominant_calculation(self, user_input: dict, calculation_result: List[Dict], ip_address: str):
        msg = self._generic_notification_message(ModuleName.PIC_CODOMINANT, user_input, calculation_result, ip_address)
        res = self.client.send_message(msg)

        return res

    def pic_dominant_calculation(self, user_input: dict, calculation_result: List[Dict], ip_address: str):
        msg = self._generic_notification_message(ModuleName.PIC_DOMINANT, user_input, calculation_result, ip_address)
        res = self.client.send_message(msg)

        return res

    def genetic_distance_calculation(self, user_input: dict, calculation_result: np.ndarray, ip_address: str):
        msg = self._generic_notification_message(
            ModuleName.GENETIC_DISTANCE, user_input, calculation_result, ip_address
        )
        res = self.client.send_message(msg)

        return res

    def chi_square_calculation(self, user_input: dict, calculation_result: List[Dict], ip_address: str):
        msg = self._generic_notification_message(ModuleName.CHI_SQUARE, user_input, calculation_result, ip_address)
        res = self.client.send_message(msg)

        return res

    def chi_square_goodness_calculation(self, user_input: dict, calculation_result: List[Dict], ip_address: str):
        msg = self._generic_notification_message(
            ModuleName.CHI_SQUARE_GOODNESS, user_input, calculation_result, ip_address
        )
        res = self.client.send_message(msg)

        return res

    def dot_plot_raw_seq_calculation(self, user_input: dict, calculation_result: List[Dict], ip_address: str):
        msg = self._generic_notification_message(
            ModuleName.DOT_PLOT_RAW_SEQ, user_input, calculation_result, ip_address
        )
        res = self.client.send_message(msg)

        return res

    def dot_plot_genebank_calculation(self, user_input: dict, calculation_result: List[Dict], ip_address: str):
        msg = self._generic_notification_message(
            ModuleName.DOT_PLOT_GENEBANK_IDS, user_input, calculation_result, ip_address
        )
        res = self.client.send_message(msg)

        return res

    def consensus_sequence_raw_seq_calculation(self, user_input: dict, calculation_result: List[Dict], ip_address: str):
        msg = self._generic_notification_message(
            ModuleName.CONSENSUS_SEQUENCE_RAW_SEQ, user_input, calculation_result, ip_address
        )
        res = self.client.send_message(msg)

        return res

    def consensus_sequence_file_seq_calculation(
        self, user_input: dict, calculation_result: List[Dict], ip_address: str
    ):
        msg = self._generic_notification_message(
            ModuleName.CONSENSUS_SEQUENCE_FILE_SEQ, user_input, calculation_result, ip_address
        )
        res = self.client.send_message(msg)

        return res

    def consensus_sequence_genebank_calculation(
        self, user_input: dict, calculation_result: List[Dict], ip_address: str
    ):
        msg = self._generic_notification_message(
            ModuleName.CONSENSUS_SEQUENCE_GENE_BANK, user_input, calculation_result, ip_address
        )
        res = self.client.send_message(msg)

        return res

    def sequences_tool_calculation(self, user_input: dict, calculation_result: List[Dict], ip_address: str):
        msg = self._generic_notification_message(ModuleName.SEQUENCES_TOOLS, user_input, calculation_result, ip_address)
        res = self.client.send_message(msg)

        return res

    def apmc_pre_train_calculation(
        self, user: Customer, project_name: str, filename: str, model_type: str, normalization: str, ip_address: str
    ):
        dt_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        msg = (
            f":bangbang: New calculation from *APMC Pre Train* :rocket:\n\n"
            + f":male-technologist: *User:* {user.email}\n"
            + f"*Project name:* {project_name}\n"
            + f"*File name:* {filename}\n"
            + f"*Model type:* {model_type}\n"
            + f"*Normalization:* {normalization}\n"
            + f":globe_with_meridians: *IP Address:* `{ip_address}`\n"
            + f":date: *Date:* `{dt_now}`\n"
        )

        res = self.client.send_message(msg)

        return res

    def apmc_train_calculation(self, user: Customer, user_input: dict, ip_address: str):
        dt_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        msg = (
            f":bangbang: New calculation from *APMC Train* :rocket:\n\n"
            + f":male-technologist: *User:* {user.email}\n"
            + f":male-technologist: *User input:*\n"
            + f"```{self._format_user_input(user_input)}```\n\n"
            + f":globe_with_meridians: *IP Address:* `{ip_address}`\n"
            + f":date: *Date:* `{dt_now}`\n"
        )

        res = self.client.send_message(msg)

        return res

    def apmc_made_prediction(self, user: Customer, apmc_model: APMCData):
        msg = (
            f":bangbang: *User:* {user.email} do a prediction on model: \n"
            + f"*Model ID:* {apmc_model.id} \n"
            + f"*Project name:* {apmc_model.project_name}\n"
            + f"*Model instance:* {apmc_model}"
        )
        res = self.client.send_message(msg)

        return res

    def apmc_report_downloaded(self, user: Customer, apmc_model: APMCData):
        msg = (
            f":bangbang: *User:* {user.email} downloaded statistical report for model: \n"
            + f"*Model ID:* {apmc_model.id} \n"
            + f"*Project name:* {apmc_model.project_name}\n"
            + f"*Model instance:* {apmc_model}"
        )
        res = self.client.send_message(msg)

        return res

    def apmc_tree_graph_downloaded(self, user: Customer, apmc_model: APMCData):
        msg = (
            f":bangbang: *User:* {user.email} downloaded tree graph for model: \n"
            + f"*Model ID:* {apmc_model.id} \n"
            + f"*Project name:* {apmc_model.project_name}\n"
            + f"*Model instance:* {apmc_model}"
        )
        res = self.client.send_message(msg)

        return res
