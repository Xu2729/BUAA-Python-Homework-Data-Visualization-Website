from django.shortcuts import render, redirect, HttpResponse
from statistic.util import make_pie, make_bar, make_radar, require_login
from django.contrib.auth.hashers import make_password, check_password
from statistic.models import User


# Create your views here.

@require_login()
def index(request):
    if request.GET.get("file") == "true":
        return render(request, "index.html", {"filename": "temp.csv"})
    return render(request, "index.html", {"filename": "students_data_FIX.csv"})


def show_pie(request):
    file_name = "statistic/data/" + request.GET.get("filename")
    key = request.GET.get("key")
    make_pie(file_name, key, None, "statistic/templates/cache/show_pie_{}.html".format(key))
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
    make_bar(file_name, key, group_by, use_stack, None,
             "statistic/templates/cache/show_bar_{}_{}_{}.html".format(key, group_by, use_stack))
    return render(request, "cache/show_bar_{}_{}_{}.html".format(key, group_by, use_stack))


def show_radar(request):
    pks = list(map(int, request.GET.get("pk").split(",")))
    file_name = "statistic/data/" + request.GET.get("filename")
    make_radar(file_name, pks,
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
