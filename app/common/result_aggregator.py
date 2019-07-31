from app.common.constants import NameConverter


def add_result(obj, name, value):
    if not hasattr(obj, 'results'):
        raise AttributeError(f"Object {obj} don't have attribute results")

    name = NameConverter.SHORTCUT_TO_MODULE_NAME.get(name, name)
    obj.results.append({'name': name, 'value': value})
