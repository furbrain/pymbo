import os.path
import importlib.util


def find_module(path, level, from_file, initial_file):
    if path is None:
        path = ''
    if level > 0:
        possible_path = get_possible_path(path, from_file, level)
    else:
        possible_path = get_possible_path(path, initial_file)
    if os.path.isdir(possible_path):
        possible_path = os.path.join(possible_path, '__init__')
    possible_path += '.py'
    if os.path.exists(possible_path):
        return possible_path
    else:
        if level == 0:
            return get_builtin_module(path)
    return None

def get_possible_path(path, starting_file, levels=0):
    starting_dir = os.path.dirname(starting_file)
    while levels > 1:
        starting_dir = os.path.dirname(starting_dir)
        levels -= 1
    file_path = os.path.join(*path.split('.'))
    possible_path = os.path.join(starting_dir, file_path)
    return possible_path

def get_builtin_module(path):
    try:
        spec = importlib.util.find_spec(path)
    except:
        return None
    if is_valid_spec(spec):
        return spec.origin
    else:
        return None

def is_valid_spec(spec):
    if spec:
        if spec.origin:
            if spec.origin.endswith('.py'):
                return True
    return False
