from django.urls import path

from core.views import (
    JobApplicationView,
    index,
    register,
    login_view,
    logout_view,
    FreelancerListView,
    FreelancerDetailView,
    EmployerDetailView,
    JobDetailView,
    JobListView,
)

app_name = "core"


urlpatterns = [
    path("", index, name="home"),
    path("jobapplication/", JobApplicationView.as_view(), name="jobappl"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("freelancer/<int:pk>/", FreelancerDetailView.as_view(), name="freelancer"),
    path("freelancers/", FreelancerListView.as_view(), name="freelancers"),
    path("jobs/", JobListView.as_view(), name="jobs"),
    path("job/<int:pk>/", JobDetailView.as_view(), name="job"),
    path("employer/<int:pk>/", EmployerDetailView.as_view(), name="employer"),
]





