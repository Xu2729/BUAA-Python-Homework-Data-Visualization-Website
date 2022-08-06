import pandas as pd
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
