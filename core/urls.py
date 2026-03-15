from django.urls import path

from core.views import (
    JobApplicationView,
    index,
    register,

)

app_name = "core"


urlpatterns = [
    path("", index, name="home"),
    path("jobapplication/", JobApplicationView.as_view(), name="jobappl"),
    path("register/", register, name="register"),
]

