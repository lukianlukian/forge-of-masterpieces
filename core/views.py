from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic

from core.forms import RegisterForm
from core.models import (
    JobApplication,
    FreelancerProfile,
    EmployerProfile, JobOffer,
)

def index(request: HttpRequest) -> HttpResponse:
    num_freelancers = FreelancerProfile.objects.count()
    num_employers = EmployerProfile.objects.count()
    context = {
        "num_freelancers": num_freelancers,
        "num_employers": num_employers,
    }
    return render(request, "core/home.html", context=context)

class JobApplicationView(LoginRequiredMixin, generic.ListView):
    model = JobApplication
    paginate_by = 10


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_freelancer:
                FreelancerProfile.objects.create(user=user)
            else:
                EmployerProfile.objects.create(user=user)
            return redirect("core:home")
    else:
        form = RegisterForm()
    return render(request, "core/register.html", {"form": form})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("core:home")
    else:
        form = AuthenticationForm()
    return render(request, "core/login.html", {"form": form})

def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("core:home")


class FreelancerListView(generic.ListView):
    model = FreelancerProfile
    template_name = "core/freelancer_list.html"
    context_object_name = "freelancers"
    paginate_by = 10
    def get_queryset(self):
        return FreelancerProfile.objects.select_related("user").prefetch_related("skills")

class FreelancerDetailView(generic.DetailView):
    model = FreelancerProfile
    template_name = "core/freelancer_detail.html"
    context_object_name = "freelancer"


class EmployerDetailView(generic.DetailView):
    model = EmployerProfile
    template_name = "core/employer_detail.html"
    context_object_name = "employer"


class JobListView(generic.ListView):
    model = JobOffer
    template_name = "core/job_list.html"
    paginate_by = 10
    context_object_name = "jobs"
    def get_queryset(self):
        return JobOffer.objects.select_related("employer")


class JobDetailView(generic.DetailView):
    model = JobOffer
    template_name = "core/job_detail.html"
    context_object_name = "job"

