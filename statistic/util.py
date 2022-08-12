import re
from django.shortcuts import redirect, render
from django.http import HttpRequest


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


def redict_error(request: HttpRequest, error_msg: str, next_url=None):
    if next_url is None:
        next_url = request.path
    return render(request, "error.html", {"error_msg": error_msg, "next": next_url})


def parse_parameter(request, key_type: dict):
    filter_dict = {}
    if request.POST.get("filter-perm") == "true":
        filter_num = int(request.POST.get("filterBoxNum"))
        for i in range(filter_num):
            k = request.POST.get("filter-key-" + str(i + 1))
            v = request.POST.getlist("filter-value-" + str(i + 1), [])
            if "" in v:
                v.remove("")
            if key_type[k] == "int":
                filter_dict[k] = patten_range(v[0])
            elif key_type[k] == "float":
                filter_dict[k] = patten_range(v[0], True)
            else:
                filter_dict[k] = v
    key = request.POST.get("chart-classify")
    chart_type = request.POST.get("chart-type")
    group_by = request.POST.get("chart-group")
    if group_by == "Default":
        group_by = None
    mark_data = request.POST.getlist("check-box")
    mark_dict = {}
    for k in ["average", "max", "min"]:
        if k in mark_data:
            mark_dict[k] = True
        else:
            mark_dict[k] = False
    return filter_dict, chart_type, key, group_by, mark_dict


def patten_range(s: str, is_float=False) -> list:
    s = re.sub(r"\s+", "", s)
    tot = s.split(";")
    ans = []
    for v in tot:
        if "-" in v:
            if is_float:
                a, b = v.split("-")
                a = float(a) - 1e-9
                b = float(b) + 1e-9
                ans.append({"min": a, "max": b, "type": "[]"})
            else:
                a, b = v.split("-")
                a = int(a)
                b = int(b)
                ans.append({"min": a, "max": b, "type": "[]"})
        elif "," in v:
            if is_float:
                a, b = v[1:-1].split(",")
                a = float(a) - 1e-9 if v[0] == "[" else float(a)
                b = float(b) + 1e-9 if v[-1] == "]" else float(b)
                ans.append({"min": a, "max": b, "type": v[0] + v[-1]})
            else:
                a, b = v[1:-1].split(",")
                a = int(a)
                b = int(b)
                ans.append({"min": a, "max": b, "type": v[0] + v[-1]})
        else:
            if is_float:
                a = float(v) - 1e-9
                b = float(v) + 1e-9
                ans.append({"min": a, "max": b, "type": "[]"})
            else:
                ans.append(int(v))
    return ans
