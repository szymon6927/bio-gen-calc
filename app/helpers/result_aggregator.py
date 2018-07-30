def add_result(obj, name, value):
    if hasattr(obj, 'results'):
        obj.results.append({'name': name, 'value': value})
    else:
        print(f'Object {obj} has no attr results', flush=True)

