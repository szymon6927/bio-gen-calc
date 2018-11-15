from app import app
from ast import literal_eval

def to_dict(string):
    return literal_eval(string)

app.jinja_env.filters['to_dict'] = to_dict
