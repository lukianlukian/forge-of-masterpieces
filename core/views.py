from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic

from core.forms import (
    RegisterForm,
    FreelancerProfileForm,
    EmployerProfileForm,
    JobOfferForm,
    JobApplicationForm,
    MessageForm,
    ReviewForm,
    AvatarForm,
)
from core.models import (
    User,
    FreelancerProfile,
    EmployerProfile,
    JobOffer,
    JobApplication,
    Message,
    Review,
)


# Home

def index(request: HttpRequest) -> HttpResponse:
    context = {
        "num_freelancers": FreelancerProfile.objects.count(),
        "num_employers": EmployerProfile.objects.count(),
        "num_jobs": JobOffer.objects.filter(status=JobOffer.OPEN).count(),
        "recent_jobs": (
            JobOffer.objects
            .filter(status=JobOffer.OPEN)
            .select_related("employer")
            .order_by("-created_at")[:6]
        ),
    }
    return render(request, "core/home.html", context)


# Auth
def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_freelancer:
                FreelancerProfile.objects.create(user=user)
            else:
                EmployerProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("core:home")
    else:
        form = RegisterForm()
    return render(request, "core/register.html", {"form": form})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.GET.get("next", "core:home"))
    else:
        form = AuthenticationForm()
    return render(request, "core/login.html", {"form": form})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("core:home")


# Freelancer

class FreelancerListView(generic.ListView):
    model = FreelancerProfile
    template_name = "core/freelancer_list.html"
    paginate_by = 12
    context_object_name = "freelancers"

    def get_queryset(self):
        qs = FreelancerProfile.objects.select_related("user").prefetch_related("skills")
        skill = self.request.GET.get("skill")
        if skill:
            qs = qs.filter(skills__name__icontains=skill)
        return qs


class FreelancerDetailView(generic.DetailView):
    model = FreelancerProfile
    template_name = "core/freelancer_detail.html"
    context_object_name = "freelancer"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["reviews"] = (
            Review.objects
            .filter(reviewee=self.object.user)
            .select_related("reviewer")
            .order_by("-created_at")
        )
        ctx["review_form"] = ReviewForm()
        return ctx


@login_required
def edit_freelancer_profile(request: HttpRequest) -> HttpResponse:
    profile = get_object_or_404(FreelancerProfile, user=request.user)
    form = FreelancerProfileForm(request.POST or None, instance=profile)
    avatar_form = AvatarForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == "POST" and form.is_valid() and avatar_form.is_valid():
        form.save()
        avatar_form.save()
        messages.success(request, "Profile updated!")
        return redirect("core:freelancer-detail", pk=profile.pk)
    return render(request, "core/edit_profile.html", {"form": form, "avatar_form": avatar_form})


# Employer

class EmployerDetailView(generic.DetailView):
    model = EmployerProfile
    template_name = "core/employer_detail.html"
    context_object_name = "employer"

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.user:
            obj.page_views += 1
            obj.save(update_fields=["page_views"])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["open_jobs"] = JobOffer.objects.filter(
            employer=self.object.user, status=JobOffer.OPEN
        )
        ctx["is_owner"] = self.request.user == self.object.user
        return ctx


@login_required
def edit_employer_profile(request: HttpRequest) -> HttpResponse:
    profile = get_object_or_404(EmployerProfile, user=request.user)
    form = EmployerProfileForm(request.POST or None, instance=profile)
    avatar_form = AvatarForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == "POST" and form.is_valid() and avatar_form.is_valid():
        form.save()
        avatar_form.save()
        messages.success(request, "Profile updated!")
        return redirect("core:employer-detail", pk=profile.pk)
    return render(request, "core/edit_profile.html", {"form": form, "avatar_form": avatar_form})


# Jobs

class JobListView(generic.ListView):
    model = JobOffer
    template_name = "core/job_list.html"
    paginate_by = 10
    context_object_name = "jobs"

    def get_queryset(self):
        qs = JobOffer.objects.select_related("employer").prefetch_related("skills_required")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs.order_by("-created_at")


class JobDetailView(generic.DetailView):
    model = JobOffer
    template_name = "core/job_detail.html"
    context_object_name = "job"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["application_form"] = JobApplicationForm()
        ctx["applications"] = self.object.applications.select_related("freelancer")
        if self.request.user.is_authenticated:
            ctx["already_applied"] = JobApplication.objects.filter(
                job=self.object, freelancer=self.request.user
            ).exists()
        return ctx


@login_required
def create_job(request: HttpRequest) -> HttpResponse:
    if not request.user.is_employer:
        return HttpResponseForbidden("Only employers can post jobs.")
    form = JobOfferForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        job = form.save(commit=False)
        job.employer = request.user
        job.save()
        form.save_m2m()
        messages.success(request, "Job offer published!")
        return redirect("core:job-detail", pk=job.pk)
    return render(request, "core/job_form.html", {"form": form, "action": "Create"})


@login_required
def edit_job(request: HttpRequest, pk: int) -> HttpResponse:
    job = get_object_or_404(JobOffer, pk=pk, employer=request.user)
    form = JobOfferForm(request.POST or None, instance=job)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Job offer updated!")
        return redirect("core:job-detail", pk=job.pk)
    return render(request, "core/job_form.html", {"form": form, "action": "Edit"})


@login_required
def delete_job(request: HttpRequest, pk: int) -> HttpResponse:
    job = get_object_or_404(JobOffer, pk=pk, employer=request.user)
    if request.method == "POST":
        job.delete()
        messages.success(request, "Job offer deleted.")
        return redirect("core:jobs")
    return render(request, "core/confirm_delete.html", {"object": job, "type": "job"})


# Applications

@login_required
def apply_to_job(request: HttpRequest, pk: int) -> HttpResponse:
    job = get_object_or_404(JobOffer, pk=pk)
    if not request.user.is_freelancer:
        messages.error(request, "Only freelancers can apply.")
        return redirect("core:job-detail", pk=pk)
    if JobApplication.objects.filter(job=job, freelancer=request.user).exists():
        messages.warning(request, "You already applied to this job.")
        return redirect("core:job-detail", pk=pk)
    form = JobApplicationForm(request.POST)
    if form.is_valid():
        app = form.save(commit=False)
        app.job = job
        app.freelancer = request.user
        app.save()
        messages.success(request, "Application submitted!")
    return redirect("core:job-detail", pk=pk)


@login_required
def update_application_status(request: HttpRequest, pk: int) -> HttpResponse:
    application = get_object_or_404(JobApplication, pk=pk)
    if application.job.employer != request.user:
        return HttpResponseForbidden()
    new_status = request.POST.get("status")
    if new_status in [JobApplication.ACCEPTED, JobApplication.REJECTED, JobApplication.PENDING]:
        application.status = new_status
        application.save(update_fields=["status"])
        messages.success(request, f"Application marked as {new_status}.")
    return redirect("core:job-detail", pk=application.job.pk)


@login_required
def my_applications(request: HttpRequest) -> HttpResponse:
    apps = (
        JobApplication.objects
        .filter(freelancer=request.user)
        .select_related("job", "job__employer")
        .order_by("-created_at")
    )
    return render(request, "core/my_applications.html", {"applications": apps})


# Messages

@login_required
def inbox(request: HttpRequest) -> HttpResponse:
    user = request.user
    partner_ids = Message.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).values_list("sender_id", "receiver_id")

    ids = set()
    for s, r in partner_ids:
        ids.add(s)
        ids.add(r)
    ids.discard(user.pk)

    partners = User.objects.filter(pk__in=ids)
    unread_counts = {
        p.pk: Message.objects.filter(sender=p, receiver=user, is_read=False).count()
        for p in partners
    }
    return render(request, "core/inbox.html", {
        "partners": partners,
        "unread_counts": unread_counts,
    })


@login_required
def conversation(request: HttpRequest, user_id: int) -> HttpResponse:
    other = get_object_or_404(User, pk=user_id)
    user = request.user
    msgs = Message.objects.filter(
        Q(sender=user, receiver=other) | Q(sender=other, receiver=user)
    ).order_by("created_at")

    # Mark incoming messages as read
    msgs.filter(sender=other, is_read=False).update(is_read=True)

    form = MessageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        m = form.save(commit=False)
        m.sender = user
        m.receiver = other
        m.save()
        return redirect("core:conversation", user_id=other.pk)

    return render(request, "core/conversation.html", {
        "messages_qs": msgs,
        "other": other,
        "form": form,
    })


# Reviews

@login_required
def add_review(request: HttpRequest, user_id: int) -> HttpResponse:
    reviewee = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewee = reviewee
            review.save()
            messages.success(request, "Review submitted!")
    return redirect(request.META.get("HTTP_REFERER", "core:home"))


# kept for backwards compat (was in your original urls.py)

class JobApplicationView(LoginRequiredMixin, generic.ListView):
    model = JobApplication
    template_name = "core/my_applications.html"
    context_object_name = "applications"
    paginate_by = 10

    def get_queryset(self):
        return JobApplication.objects.filter(freelancer=self.request.user).order_by("-created_at")
