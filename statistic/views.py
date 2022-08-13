from django.shortcuts import render, redirect, HttpResponse
from statistic.draw import draw_pie, draw_bar, draw_radar, draw_line, draw_frequency_histogram
from statistic.util import require_login, redict_error, parse_parameter
from statistic.data_process import my_filter, analysis_file, select_data
from django.contrib.auth.hashers import make_password, check_password
from statistic.models import User
from statistic.predict import predict_class
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
    key_type, args_dict["key_value"], args_dict["key_description"], ori_data = analysis_file(tot_filename)
    args_dict["key_type"] = key_type
    args_dict["tot_size"] = len(ori_data)
    args_dict["pic_num"] = 1
    if request.method == "GET":
        ori_data.to_csv('statistic/data/_filter.csv', index=True, index_label="id")
        args_dict["pic_url"] = "/show_pie/?filename=" + args_dict["filename"] + "&key=Topic"
        return render(request, "index.html", args_dict)

    filter_dict, chart_type, key, group_by, mark_dict = parse_parameter(request, key_type)
    _, _, args_dict["key_description"], new_data = analysis_file(tot_filename, filter_dict)
    args_dict["tot_size"] = len(new_data)

    if len(new_data) == 0:
        return redirect(request, "no matching data")

    if chart_type == "1":
        pic_name = "cache/show_pie_{}.html".format(key)
        draw_pie(new_data, key, group_by, None, save_filename="statistic/templates/" + pic_name)
        args_dict["pic_num"] = len(new_data[group_by].value_counts())
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
        args_dict["pic_num"] = len(new_data[group_by].value_counts())

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
    group_by = request.GET.get("group_by")
    data = my_filter(file_name, **{})
    draw_pie(data, key, group_by, None, save_filename="statistic/templates/cache/show_pie_{}.html".format(key))
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
        return redict_error(request, "Illegal access", "/index/")
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith(".csv"):
            return redict_error(request, "Wrong file type", "/index/")
        if csv_file.multiple_chunks():
            return redict_error(request, "File size exceeds limit(2.5MB)", "/index/")
        with open('statistic/data/temp.csv', 'wb') as f:
            for line in csv_file.chunks():
                f.write(line)
        return redirect('/index/?file=true')
    except Exception as e:
        print(e)
        return redict_error(request, "An error occurred while saving the file", "/index/")


def download_csv(request):
    if request.method != "GET":
        return redict_error(request, "Illegal access", "/index/")
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
    return render(request, "error.html", {"error_msg": "Illegal access", "next": "/index/"})


def predict(request):
    if request.method == "GET":
        return render(request, "predict.html")
    para_dict = {"gender": request.POST.get("gender"), "Topic": request.POST.get("Topic"),
                 "raisedhands": int(request.POST.get("raisedhands")),
                 "VisitedResources": int(request.POST.get("VisitedResources")),
                 "AnnouncementsView": int(request.POST.get("AnnouncementsView")),
                 "Nationality": "Iraq", "PlaceofBirth": "Iraq", "GradeID": "G-08", "Semester": "F", "Relation": "Mum",
                 "Discussion": 100, "StudentAbsenceDays": "Under-7", "ParentschoolSatisfaction": "Bad",
                 "ParentAnsweringSurvey": "Yes"}
    result = predict_class(para_dict)
    return render(request, "predict.html", {"result": result})


def test(request):
    return render(request, "pic_test.html")


def page_not_found(request, exception):
    return redict_error(request, "Page not found", "/index/")


def display(request):
    res_dict = {"show": False}
    if request.method == "GET":
        return render(request, "display.html")
    students = request.POST.get("student-id")
    students = students.split(",")
    students = list(map(int, students))
    data = my_filter("statistic/data/students_data_FIX.csv", **{})
    data_head, data_body = select_data(data, students)
    res_dict["data_head"] = data_head
    res_dict["data_body"] = data_body
    res_dict["show"] = True
    draw_radar(data, students,
               {"raisedhands": 100, "VisitedResources": 100, "AnnouncementsView": 100, "Discussion": 100}, None,
               save_filename="statistic/templates/cache/radar_display.html")
    return render(request, "display.html", res_dict)
