import pandas as pd
from pandas import DataFrame
from django.shortcuts import redirect
from django.http import HttpRequest


def get_table_keys(data_filename: str) -> list:
    with open(data_filename, "r") as f:
        line = f.readline()
    return line[:-1].split(",")


def get_table_key_values(data_filename: str) -> dict:
    data = pd.read_csv(data_filename)
    res = {}
    keys = get_table_keys(data_filename)
    for k in keys:
        res[k] = list(dict(data[k].value_counts()).keys())
    return res


def analysis_file(filename: str):
    data = pd.read_csv(filename)
    keys = data.columns
    key_type = {}
    key_values = {}
    for key in keys:
        if data[key].dtype == "object":
            key_type[key] = "obj"
            key_values[key] = list(set(data[key].values))
            key_values[key].sort()
        elif data[key].dtype == "int64":
            if len(set(data[key].values)) > 10:
                key_type[key] = "int"
                key_values[key] = {"max": max(data[key].values), "min": min(data[key].values)}
            else:
                key_type[key] = "obj"
                key_values[key] = list(set(data[key].values))
                key_values[key].sort()
        elif data[key].dtype == "float64":
            key_type[key] = "float"
            key_values[key] = {"max": max(data[key].values), "min": min(data[key].values)}
    return key_type, key_values


def require_login():
    def decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            cookies = request.COOKIES
            is_login = cookies.get("is_login")
            if is_login == "True":
                return func(request, *args, **kwargs)
            else:
                return redirect("/login/?next={}".format(request.path))

        return wrapper

    return decorator


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
            for v in range_list:
                if v["type"] == "()" and v["min"] < x < v["max"]:
                    return True
                elif v["type"] == "[)" and v["min"] <= x < v["max"]:
                    return True
                elif v["type"] == "(]" and v["min"] < x <= v["max"]:
                    return True
                elif v["type"] == "[]" and v["min"] <= x <= v["max"]:
                    return True
        return False

    return inner
