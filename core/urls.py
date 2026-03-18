from django.urls import path

from core.views import (
    # kept from your original file
    JobApplicationView,
    index,
    register,
    login_view,
    logout_view,
    FreelancerDetailView,
    EmployerDetailView,
    JobDetailView,
    JobListView,
    # new
    FreelancerListView,
    edit_freelancer_profile,
    edit_employer_profile,
    create_job,
    edit_job,
    delete_job,
    apply_to_job,
    update_application_status,
    my_applications,
    inbox,
    conversation,
    add_review,
)

app_name = "core"

urlpatterns = [
    # Home
    path("", index, name="home"),

    # Auth
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # Freelancers
    path("freelancers/", FreelancerListView.as_view(), name="freelancer-list"),
    path("freelancer/<int:pk>/", FreelancerDetailView.as_view(), name="freelancer-detail"),
    path("freelancer/edit/", edit_freelancer_profile, name="edit-freelancer"),

    # Employers
    path("employer/<int:pk>/", EmployerDetailView.as_view(), name="employer-detail"),
    path("employer/edit/", edit_employer_profile, name="edit-employer"),

    # Jobs
    path("jobs/", JobListView.as_view(), name="jobs"),
    path("job/<int:pk>/", JobDetailView.as_view(), name="job-detail"),
    path("job/create/", create_job, name="job-create"),
    path("job/<int:pk>/edit/", edit_job, name="job-edit"),
    path("job/<int:pk>/delete/", delete_job, name="job-delete"),

    # Applications
    path("job/<int:pk>/apply/", apply_to_job, name="apply"),
    path("application/<int:pk>/status/", update_application_status, name="application-status"),
    path("my-applications/", my_applications, name="my-applications"),

    # Messages
    path("inbox/", inbox, name="inbox"),
    path("inbox/<int:user_id>/", conversation, name="conversation"),

    # Reviews
    path("review/<int:user_id>/", add_review, name="add-review"),
]
