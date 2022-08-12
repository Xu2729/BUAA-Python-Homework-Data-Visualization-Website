from django.shortcuts import render, redirect, HttpResponse
from statistic.draw import draw_pie, draw_bar, draw_radar, draw_line, draw_frequency_histogram
from statistic.util import require_login, redict_error
from statistic.data_process import my_filter, analysis_file, patten_range
from django.contrib.auth.hashers import make_password, check_password
from statistic.models import User
import csv


# Create your views here.

@require_login()
def index(request):
    args_dict = {}
    tot_filename = "statistic/data/"
    if request.GET.get("file") == "true":
        args_dict["filename"] = "temp.csv"
        tot_filename += "temp.csv"
    else:
        args_dict["filename"] = "students_data_FIX.csv"
        tot_filename += "students_data_FIX.csv"
    key_type, key_value, key_description, ori_data = analysis_file(tot_filename)
    args_dict["key_type"] = key_type
    args_dict["key_value"] = key_value
    args_dict["key_description"] = key_description
    args_dict["tot_size"] = len(ori_data)
    if request.method == "GET":
        ori_data.to_csv('statistic/data/_filter.csv', index=True, index_label="id")
        args_dict["pic_url"] = "/show_pie/?filename=" + args_dict["filename"] + "&key=Topic"
        return render(request, "index.html", args_dict)
    filter_dict = {}
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
    _, _, key_description, new_data = analysis_file(tot_filename, filter_dict)
    args_dict["key_description"] = key_description
    args_dict["tot_size"] = len(new_data)
    mark_data = request.POST.getlist("check-box")
    mark_dict = {}
    for k in ["average", "max", "min"]:
        if k in mark_data:
            mark_dict[k] = True
        else:
            mark_dict[k] = False
    if len(new_data) == 0:
        return redirect(request, "no matching data")
    if chart_type == "1":
        pic_name = "cache/show_pie_{}.html".format(key)
        draw_pie(new_data, key, group_by, None, save_filename="statistic/templates/" + pic_name)
    elif chart_type == "2":
        pic_name = "cache/show_bar_{}.html".format(key)
        draw_bar(new_data, key, group_by, mark_dict=mark_dict, save_filename="statistic/templates/" + pic_name)
    elif chart_type == "3":
        pic_name = "cache/show_line_{}.html".format(key)
        draw_line(new_data, key, group_by, mark_dict=mark_dict, save_filename="statistic/templates/" + pic_name)
    else:
        pic_name = "cache/show_frequency_histogram_{}.html".format(key)
        space = int(request.POST.get("space"))
        draw_frequency_histogram(new_data, key, space, group_by, mark_dict=mark_dict,
                                 save_filename="statistic/templates/" + pic_name)
    args_dict["pic_url"] = "/find/?path=" + pic_name
    new_data.to_csv("statistic/data/_filter.csv", index=True, index_label="id")
    return render(request, "index.html", args_dict)


def find(request):
    path = request.GET.get("path")
    return render(request, path)


def login(request):
    next_url = request.GET.get("next")
    if request.method == "GET":
        return render(request, "login.html", {"next_url": next_url})
    user = request.POST.get("user")
    pwd = request.POST.get("password")
    if not User.objects.filter(name=user).exists():
        return render(request, "login.html", {"error_msg": "user doesn't exist"})
    if not check_password(pwd, User.objects.get(name=user).password):
        return render(request, "login.html", {"error_msg": "password error"})
    res = redirect(next_url)
    res.set_cookie("is_login", True)
    res.set_cookie("user", user)
    return res


def logout(request):
    res = redirect("/login/?next=/index/")
    res.set_cookie("is_login", False)
    return res


def show_pie(request):
    file_name = "statistic/data/" + request.GET.get("filename")
    key = request.GET.get("key")
    data = my_filter(file_name, **{})
    draw_pie(data, key, None, "statistic/templates/cache/show_pie_{}.html".format(key))
    return render(request, "cache/show_pie_{}.html".format(key))


def show_bar(request):
    key = request.GET.get("key")
    file_name = "statistic/data/" + request.GET.get("filename")
    group_by = request.GET.get("group_by")
    if group_by == "null":
        group_by = None
    use_stack = request.GET.get("use_stack")
    if use_stack == "true":
        use_stack = True
    else:
        use_stack = False
    data = my_filter(file_name, **{})
    draw_bar(data, key, group_by, use_stack, False, None,
             "statistic/templates/cache/show_bar_{}_{}_{}.html".format(key, group_by, use_stack))
    return render(request, "cache/show_bar_{}_{}_{}.html".format(key, group_by, use_stack))


def show_radar(request):
    pks = list(map(int, request.GET.get("pk").split(",")))
    file_name = "statistic/data/" + request.GET.get("filename")
    data = my_filter(file_name, **{})
    draw_radar(data, pks,
               {"raisedhands": 100, "VisitedResources": 100, "AnnouncementsView": 100, "Discussion": 100}, None,
               "statistic/templates/cache/show_radar_{}.html".format(request.GET.get("pk").replace(",", "&")))
    return render(request, "cache/show_radar_{}.html".format(request.GET.get("pk").replace(",", "&")))


def upload_csv(request):
    if request.method != "POST":
        return redict_error(request, "illegal access", "/index/")
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith(".csv"):
            return redict_error(request, "wrong file type", "/index/")
        if csv_file.multiple_chunks():
            return redict_error(request, "file size exceeds limit(2.5MB)", "/index/")
        with open('statistic/data/temp.csv', 'wb') as f:
            for line in csv_file.chunks():
                f.write(line)
        return redirect('/index/?file=true')
    except Exception as e:
        print(e)
        return HttpResponse("保存文件时发生错误")


def download_csv(request):
    if request.method != "GET":
        return redict_error(request, "illegal access", "/index/")
    res = HttpResponse(content_type="text/csv")
    res["Content-Disposition"] = "attachment; filename=\"selectData.csv"
    writer = csv.writer(res)
    with open("statistic/data/" + request.GET.get("file"), "r") as f:
        reader = csv.reader(f)
        writer.writerows(reader)
    return res


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    user = request.POST.get("user")
    pwd = request.POST.get("password")
    email = request.POST.get("email")
    mobile = request.POST.get("mobile")
    introduction = request.POST.get("introduction")
    User.objects.create(name=user, password=make_password(pwd, None, 'pbkdf2_sha256'), email=email, mobile=mobile,
                        introduction=introduction)
    return redirect("/login/?next=/index/")


def error(request):
    return render(request, "error.html", {"error_msg": "illegal access", "next": "/index/"})
