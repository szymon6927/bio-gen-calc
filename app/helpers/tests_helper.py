from .result_aggregator import name_converter


def find_value_by_name(result_list, name):
    result_dict = next((result for result in result_list if result["name"] == name))
    return result_dict.get('value')
