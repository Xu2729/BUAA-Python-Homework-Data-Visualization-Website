import pandas as pd
from pandas import DataFrame
from django.template.defaulttags import register


@register.filter
def get_dict_item(dictionary: dict, key):
    return dictionary.get(key)


@register.filter
def get_list_item(my_list: list, index):
    if index >= len(my_list):
        return None
    else:
        return my_list[index]


def analysis_file(filename: str, filter_dict=None):
    if filter_dict is None:
        data = pd.read_csv(filename)
        data["Class"] = data["Class"].apply(parse_class)
    else:
        data = my_filter(filename, **filter_dict)
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
            key_description[key] = get_obj_description(data, key)
        elif data[key].dtype == "int64":
            key_type[key] = "int"
            key_values[key] = {"max": max(data[key].values), "min": min(data[key].values)}
            key_description[key] = round_dict(dict(description[key]))
        elif data[key].dtype == "float64":
            key_type[key] = "float"
            key_values[key] = {"max": max(data[key].values), "min": min(data[key].values)}
            key_description[key] = round_dict(dict(description[key]))
    return key_type, key_values, key_description, data


def parse_class(x):
    if int(x) == 1:
        return "Poor"
    elif int(x) == 2:
        return "Average"
    elif int(x) == 3:
        return "Excellent"
    else:
        return "UNKNOWN"


def round_dict(d: dict):
    for k, v in d.items():
        d[k] = round(v, 2)
    return d


def get_obj_description(data: DataFrame, key: str):
    temp = dict(data[key].value_counts())
    count = len(data)
    for k, v in temp.items():
        temp[k] = int(v)
    temp = sorted(temp.items(), key=lambda x: x[1], reverse=True)
    if len(temp) > 5:
        ans = []
        sum_ = 0
        i = 0
        for ele in temp:
            if i < 5:
                ans.append({ele[0]: [str(ele[1]), "%.2f%%" % (100 * ele[1] / count)]})
            else:
                sum_ += int(ele[1])
            i += 1
        ans.append({"Others": [str(sum_), "%.2f%%" % (100 * sum_ / count)]})
    else:
        ans = [{ele[0]: [str(ele[1]), "%.2f%%" % (100 * ele[1] / count)]} for ele in temp]
    return ans


def my_filter(filename: str, **kwargs) -> DataFrame:
    data = pd.read_csv(filename)
    data["Class"] = data["Class"].apply(parse_class)
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


def select_data(data: DataFrame, pks: list):
    ans_head = ["id"]
    ans_body = []
    keys = data.columns
    for key in keys:
        ans_head.append(str(key))
    for pk in pks:
        temp_data = data.iloc[pk]
        temp = [str(pk)]
        for key in keys:
            temp.append(str(temp_data[key]))
        ans_body.append(temp)
    print(ans_head)
    print(ans_body)
    return ans_head, ans_body
