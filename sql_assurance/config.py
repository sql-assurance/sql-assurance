import sys
import os
import yaml


def find_path_to_config_parameter():
    args = sys.argv

    if 'SQLASSURANCE_CONFIG_PATH' in os.environ:
        return os.environ['SQLASSURANCE_CONFIG_PATH']

    for i, arg in enumerate(args):
        if arg[i] == 'p':
            return args[i+1]


def load_config(path):
    if not os.path.exists(path):
        raise ValueError("Path {} is not valid")

    with open(path, 'r') as context:
        config = yaml.load(context.read())
    context.close()

    return config

path_to_config_file = find_path_to_config_parameter()
settings = load_config(path_to_config_file)
