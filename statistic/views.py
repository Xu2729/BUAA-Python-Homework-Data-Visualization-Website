from django.shortcuts import render
from statistic.util import make_pie, make_bar, make_radar

# Create your views here.
DATA_FILENAME = 'statistic/data/students_data_FIX.csv'


def index(request):
    return render(request, "index.html")


def show_pie(request):
    key = request.GET.get("key")
    make_pie(DATA_FILENAME, key, None, "statistic/templates/cache/show_pie_{}.html".format(key))
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
    make_bar(DATA_FILENAME, key, group_by, use_stack, None,
             "statistic/templates/cache/show_bar_{}_{}_{}.html".format(key, group_by, use_stack))
    return render(request, "cache/show_bar_{}_{}_{}.html".format(key, group_by, use_stack))


def show_radar(request):
    pks = list(map(int, request.GET.get("pk").split(",")))
    make_radar(DATA_FILENAME, pks,
               {"raisedhands": 100, "VisitedResources": 100, "AnnouncementsView": 100, "Discussion": 100}, None,
               "statistic/templates/cache/show_radar_{}.html".format(request.GET.get("pk").replace(",", "&")))
    return render(request, "cache/show_radar_{}.html".format(request.GET.get("pk").replace(",", "&")))
