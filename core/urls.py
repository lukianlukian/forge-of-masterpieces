from django.urls import path

from core.views import (
    IndexView,
    RegisterView,
    LoginView,
    LogoutView,
    FreelancerListView,
    FreelancerDetailView,
    EditFreelancerProfileView,
    EmployerDetailView,
    EditEmployerProfileView,
    JobListView,
    JobDetailView,
    JobCreateView,
    JobEditView,
    JobDeleteView,
    ApplyToJobView,
    UpdateApplicationStatusView,
    MyApplicationsView,
    InboxView,
    ConversationView,
    AddReviewView,
)

app_name = "core"

urlpatterns = [
    # Home
    path("", IndexView.as_view(), name="home"),

    # Auth
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # Freelancers
    path("freelancers/", FreelancerListView.as_view(), name="freelancer-list"),
    path("freelancer/<int:pk>/", FreelancerDetailView.as_view(), name="freelancer-detail"),
    path("freelancer/edit/", EditFreelancerProfileView.as_view(), name="edit-freelancer"),

    # Employers
    path("employer/<int:pk>/", EmployerDetailView.as_view(), name="employer-detail"),
    path("employer/edit/", EditEmployerProfileView.as_view(), name="edit-employer"),

    # Jobs
    path("jobs/", JobListView.as_view(), name="jobs"),
    path("job/<int:pk>/", JobDetailView.as_view(), name="job-detail"),
    path("job/create/", JobCreateView.as_view(), name="job-create"),
    path("job/<int:pk>/edit/", JobEditView.as_view(), name="job-edit"),
    path("job/<int:pk>/delete/", JobDeleteView.as_view(), name="job-delete"),

    # Applications
    path("job/<int:pk>/apply/", ApplyToJobView.as_view(), name="apply"),
    path("application/<int:pk>/status/", UpdateApplicationStatusView.as_view(), name="application-status"),
    path("my-applications/", MyApplicationsView.as_view(), name="my-applications"),

    # Messages
    path("inbox/", InboxView.as_view(), name="inbox"),
    path("inbox/<int:user_id>/", ConversationView.as_view(), name="conversation"),

    # Reviews
    path("review/<int:user_id>/", AddReviewView.as_view(), name="add-review"),
]
