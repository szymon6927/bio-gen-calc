import os


def get_static_abs_path():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.dirname(current_dir)

    abs_static_path = os.path.join(parent_dir, 'static', 'uploads')
    static_path = os.path.join('/', 'static', 'uploads')
    return {'abs_static_path': abs_static_path, 'static_path': static_path}