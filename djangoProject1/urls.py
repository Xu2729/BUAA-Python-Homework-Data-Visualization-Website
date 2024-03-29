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
    path("predict/", views.predict),
    path("display/", views.display),
    path("analysis/data/analysis", views.analysis_data_analysis),
    path("analysis/data/overview", views.analysis_data_overview),
    path("analysis/data/prepocessing", views.analysis_data_preprocessing),
    path("analysis/feature/selection", views.analysis_feature_selection),
    path("analysis/model/construction", views.analysis_model_construction),
    path("analysis/model/training", views.analysis_model_training),
    path("analysis/prediction", views.analysis_prediction),

]

handler404 = views.page_not_found
handler400 = views.bad_request
handler403 = views.access_denied
handler500 = views.server_error
