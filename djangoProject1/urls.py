"""djangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from statistic import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("show_pie/", views.show_pie),
    path("show_bar/", views.show_bar),
    path("show_radar/", views.show_radar),
    path("index/", views.index),
    path("upload/csv/", views.upload_csv),
    path("login/", views.login),
    path("register/", views.register),
    path("logout/", views.logout),
    path("find/", views.find),
    path("download/csv/", views.download_csv),
    path("error/", views.error),
    # path("test/", views.test)
]
