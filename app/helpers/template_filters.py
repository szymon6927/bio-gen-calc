from app import app
from ast import literal_eval


def to_dict(string):
    return literal_eval(string)


def translate_name(name):
    if name == "amplified_marker":
        return "Number or frequency of amplified marker"
    elif name == "absecnce_marker":
        return "Number or frequency of absecnce marker"
    elif name == "width":
        return "Table width"
    elif name == "height":
        return "Table height"
    elif name == "matrix":
        return "Distance matrix"
    elif name == "dendrogram":
        return "Dendogram"
    else:
        return name


app.jinja_env.filters['to_dict'] = to_dict
app.jinja_env.filters['translate_name'] = translate_name
