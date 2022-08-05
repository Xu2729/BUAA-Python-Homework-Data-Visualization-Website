from django.shortcuts import render, redirect, HttpResponse
from statistic.draw import draw_pie, draw_bar, draw_radar
from statistic.util import require_login, get_table_keys, get_table_key_values
from statistic.data_process import my_filter, analysis_file
from django.contrib.auth.hashers import make_password, check_password
from statistic.models import User


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
    key_type, key_value, key_description = analysis_file(tot_filename)
    args_dict["table_keys"] = get_table_keys(tot_filename)
    args_dict["table_key_values"] = get_table_key_values(tot_filename)
    args_dict["key_type"] = key_type
    args_dict["key_value"] = key_value
    args_dict["key_description"] = key_description
    args_dict["url"] = request.path
    if request.method == "GET":
        args_dict["pic_url"] = "/show_pie/?filename=" + args_dict["filename"] + "&key=Topic"
        return render(request, "index.html", args_dict)
    keys = request.POST.getlist("filter-key")
    values = request.POST.getlist("filter-value")
    filter_dict = {}
    for i in range(len(keys)):
        filter_dict[keys[i]] = values[i]
    file_name = "statistic/data/" + args_dict["filename"]
    key = "Topic"
    pic_name = "cache/show_pie_{}.html".format(key)
    draw_pie(my_filter(file_name, **filter_dict), key, None, "statistic/templates/" + pic_name)
    args_dict["pic_url"] = "/find/?path=" + pic_name
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
        return render(request, "login.html", {"error_msg": "用户不存在"})
    if not check_password(pwd, User.objects.get(name=user).password):
        return render(request, "login.html", {"error_msg": "密码错误"})
    res = redirect(next_url)
    res.set_cookie("is_login", True)
    return res


def logout(request):
    res = redirect("/login/?next=/index/")
    res.set_cookie("is_login", False)
    return res


def show_pie(request):
    file_name = "statistic/data/" + request.GET.get("filename")
    key = request.GET.get("key")
    draw_pie(my_filter(file_name, **{}), key, None, "statistic/templates/cache/show_pie_{}.html".format(key))
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
    draw_bar(my_filter(file_name, **{}), key, group_by, use_stack, False, None,
             "statistic/templates/cache/show_bar_{}_{}_{}.html".format(key, group_by, use_stack))
    return render(request, "cache/show_bar_{}_{}_{}.html".format(key, group_by, use_stack))


def show_radar(request):
    pks = list(map(int, request.GET.get("pk").split(",")))
    file_name = "statistic/data/" + request.GET.get("filename")
    draw_radar(my_filter(file_name, **{}), pks,
               {"raisedhands": 100, "VisitedResources": 100, "AnnouncementsView": 100, "Discussion": 100}, None,
               "statistic/templates/cache/show_radar_{}.html".format(request.GET.get("pk").replace(",", "&")))
    return render(request, "cache/show_radar_{}.html".format(request.GET.get("pk").replace(",", "&")))


def upload_csv(request):
    if request.method != "POST":
        return HttpResponse("请求类型错误")
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith(".csv"):
            return HttpResponse("文件类型错误")
        if csv_file.multiple_chunks():
            return HttpResponse("文件大小超出限制（2.5MB）")
        with open('statistic/data/temp.csv', 'wb') as f:
            for line in csv_file.chunks():
                f.write(line)
        return redirect('/index/?file=true')
    except Exception as e:
        print(e)
        return HttpResponse("保存文件时发生错误")


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
