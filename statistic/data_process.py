import pandas as pd
from pandas import DataFrame


def analysis_file(filename: str):
    data = pd.read_csv(filename)
    keys = data.columns
    description = data.describe()
    key_type = {}
    key_values = {}
    key_description = {}
    for key in keys:
        if data[key].dtype == "object":
            key_type[key] = "obj"
            key_values[key] = list(set(data[key].values))
            key_values[key].sort()
        elif data[key].dtype == "int64":
            if len(set(data[key].values)) > 10:
                key_type[key] = "int"
                key_values[key] = {"max": max(data[key].values), "min": min(data[key].values)}
                key_description[key] = dict(description[key])
            else:
                key_type[key] = "obj"
                key_values[key] = list(set(data[key].values))
                key_values[key].sort()
        elif data[key].dtype == "float64":
            key_type[key] = "float"
            key_values[key] = {"max": max(data[key].values), "min": min(data[key].values)}
            key_description[key] = dict(description[key])
    return key_type, key_values, key_description


def my_filter(filename: str, **kwargs) -> DataFrame:
    data = pd.read_csv(filename)
    for k, v in kwargs.items():
        if isinstance(v, list):
            data = data[data[k].apply(make_func(v))]
        else:
            data = data[data[k] == v]
    return data


def make_func(select: list):
    elements = []
    range_list = []
    for v in select:
        if isinstance(v, dict):
            range_list.append(v)
        else:
            elements.append(v)
    print(range_list)

    def inner(x):
        if x in elements:
            return True
        else:
            for _v in range_list:
                if _v["type"] == "()" and _v["min"] < x < _v["max"]:
                    return True
                elif _v["type"] == "[)" and _v["min"] <= x < _v["max"]:
                    return True
                elif _v["type"] == "(]" and _v["min"] < x <= _v["max"]:
                    return True
                elif _v["type"] == "[]" and _v["min"] <= x <= _v["max"]:
                    return True
        return False

    return inner
