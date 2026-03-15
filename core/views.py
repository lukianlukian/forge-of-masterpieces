from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic

from core.forms import RegisterForm
from core.models import (
    JobApplication,
    FreelancerProfile,
    EmployerProfile,
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
