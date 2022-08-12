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
