import os
import sys

current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
import config


def get_model_name(model):
    name = str(model)
    return name[0:name.index("(")]


def get_model_by_name(name):
    for model in config.models:
        if get_model_name(model) == name:
            return model
