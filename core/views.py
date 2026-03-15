from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import generic

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
    return render(request, "core/index.html", context=context)

class JobApplicationView(LoginRequiredMixin, generic.ListView):
    model = JobApplication
    paginate_by = 10
