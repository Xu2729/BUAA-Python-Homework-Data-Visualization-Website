from django.shortcuts import render, redirect, HttpResponse
from statistic.util import make_pie, make_bar, make_radar

# Create your views here.
file_name = 'statistic/data/students_data_FIX.csv'


def index(request):
    return render(request, "index.html")


def show_pie(request):
    key = request.GET.get("key")
    make_pie(file_name, key, None, "statistic/templates/cache/show_pie_{}.html".format(key))
    return render(request, "cache/show_pie_{}.html".format(key))


def show_bar(request):
    key = request.GET.get("key")
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
    make_radar(file_name, pks,
               {"raisedhands": 100, "VisitedResources": 100, "AnnouncementsView": 100, "Discussion": 100}, None,
               "statistic/templates/cache/show_radar_{}.html".format(request.GET.get("pk").replace(",", "&")))
    return render(request, "cache/show_radar_{}.html".format(request.GET.get("pk").replace(",", "&")))


def upload_csv(request):
    global file_name
    if request.method != "POST":
        return "请求类型错误"
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith(".csv"):
            return "文件类型错误"
        if csv_file.multiple_chunks():
            return "文件大小超出限制（2.5MB）"
        with open('statistic/data/temp.csv', 'wb') as f:
            for line in csv_file.chunks():
                f.write(line)
        file_name = 'statistic/data/temp.csv'
        return redirect('/index/')
    except Exception as e:
        print(e)
        return HttpResponse("保存文件时发生错误")
