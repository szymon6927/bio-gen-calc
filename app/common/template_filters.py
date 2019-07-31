from ast import literal_eval

from app.common.constants import NameConverter


def to_dict(string):
    return literal_eval(string)


def translate_name(name):
    return NameConverter.KEY_TO_NAME.get(name, name)


def remove_first_last_double_quotes(text):
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]

        return text

    return text
