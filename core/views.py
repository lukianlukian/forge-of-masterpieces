from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from core.forms import (
    AvatarForm,
    EmployerProfileForm,
    FreelancerProfileForm,
    JobApplicationForm,
    JobOfferForm,
    MessageForm,
    RegisterForm,
    ReviewForm,
)
from core.models import (
    EmployerProfile,
    FreelancerProfile,
    JobApplication,
    JobOffer,
    Message,
    Review,
    User,
)


# Home

class IndexView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["num_freelancers"] = FreelancerProfile.objects.count()
        ctx["num_employers"] = EmployerProfile.objects.count()
        ctx["num_jobs"] = JobOffer.objects.filter(status=JobOffer.OPEN).count()
        ctx["recent_jobs"] = (
            JobOffer.objects
            .filter(status=JobOffer.OPEN)
            .select_related("employer")
            .order_by("-created_at")[:6]
        )
        return ctx


# Auth

class RegisterView(View):
    template_name = "core/register.html"

    def get(self, request):
        return self._render(request, RegisterForm())

    def post(self, request):
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
        return self._render(request, form)

    def _render(self, request, form):
        from django.shortcuts import render
        return render(request, self.template_name, {"form": form})


class LoginView(View):
    template_name = "core/login.html"

    def get(self, request):
        return self._render(request, AuthenticationForm())

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.GET.get("next", "core:home"))
        return self._render(request, form)

    def _render(self, request, form):
        from django.shortcuts import render
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("core:home")


# Freelancer

class FreelancerListView(ListView):
    model = FreelancerProfile
    template_name = "core/freelancer_list.html"
    context_object_name = "freelancers"
    paginate_by = 12

    def get_queryset(self):
        qs = FreelancerProfile.objects.select_related("user").prefetch_related("skills")
        skill = self.request.GET.get("skill")
        if skill:
            qs = qs.filter(skills__name__icontains=skill)
        return qs


class FreelancerDetailView(DetailView):
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


class EditFreelancerProfileView(LoginRequiredMixin, View):
    template_name = "core/edit_profile.html"

    def get(self, request):
        profile = get_object_or_404(FreelancerProfile, user=request.user)
        return self._render(request, profile)

    def post(self, request):
        profile = get_object_or_404(FreelancerProfile, user=request.user)
        form = FreelancerProfileForm(request.POST, instance=profile)
        avatar_form = AvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid() and avatar_form.is_valid():
            form.save()
            avatar_form.save()
            messages.success(request, "Profile updated!")
            return redirect("core:freelancer-detail", pk=profile.pk)
        return self._render(request, profile, form, avatar_form)

    def _render(self, request, profile, form=None, avatar_form=None):
        from django.shortcuts import render
        return render(request, self.template_name, {
            "form": form or FreelancerProfileForm(instance=profile),
            "avatar_form": avatar_form or AvatarForm(instance=request.user),
        })


# Employer

class EmployerDetailView(DetailView):
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


class EditEmployerProfileView(LoginRequiredMixin, View):
    template_name = "core/edit_profile.html"

    def get(self, request):
        profile = get_object_or_404(EmployerProfile, user=request.user)
        return self._render(request, profile)

    def post(self, request):
        profile = get_object_or_404(EmployerProfile, user=request.user)
        form = EmployerProfileForm(request.POST, instance=profile)
        avatar_form = AvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid() and avatar_form.is_valid():
            form.save()
            avatar_form.save()
            messages.success(request, "Profile updated!")
            return redirect("core:employer-detail", pk=profile.pk)
        return self._render(request, profile, form, avatar_form)

    def _render(self, request, profile, form=None, avatar_form=None):
        from django.shortcuts import render
        return render(request, self.template_name, {
            "form": form or EmployerProfileForm(instance=profile),
            "avatar_form": avatar_form or AvatarForm(instance=request.user),
        })


# Jobs

class JobListView(ListView):
    model = JobOffer
    template_name = "core/job_list.html"
    context_object_name = "jobs"
    paginate_by = 10

    def get_queryset(self):
        qs = JobOffer.objects.select_related("employer").prefetch_related("skills_required")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs.order_by("-created_at")


class JobDetailView(DetailView):
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


class JobCreateView(LoginRequiredMixin, View):
    template_name = "core/job_form.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_employer:
            return HttpResponseForbidden("Only employers can post jobs.")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        from django.shortcuts import render
        return render(request, self.template_name, {"form": JobOfferForm(), "action": "Create"})

    def post(self, request):
        from django.shortcuts import render
        form = JobOfferForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            form.save_m2m()
            messages.success(request, "Job offer published!")
            return redirect("core:job-detail", pk=job.pk)
        return render(request, self.template_name, {"form": form, "action": "Create"})


class JobEditView(LoginRequiredMixin, View):
    template_name = "core/job_form.html"

    def get_object(self, request, pk):
        return get_object_or_404(JobOffer, pk=pk, employer=request.user)

    def get(self, request, pk):
        from django.shortcuts import render
        job = self.get_object(request, pk)
        return render(request, self.template_name, {"form": JobOfferForm(instance=job), "action": "Edit"})

    def post(self, request, pk):
        from django.shortcuts import render
        job = self.get_object(request, pk)
        form = JobOfferForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job offer updated!")
            return redirect("core:job-detail", pk=job.pk)
        return render(request, self.template_name, {"form": form, "action": "Edit"})


class JobDeleteView(LoginRequiredMixin, View):
    template_name = "core/confirm_delete.html"

    def get_object(self, request, pk):
        return get_object_or_404(JobOffer, pk=pk, employer=request.user)

    def get(self, request, pk):
        from django.shortcuts import render
        job = self.get_object(request, pk)
        return render(request, self.template_name, {"object": job, "type": "job"})

    def post(self, request, pk):
        job = self.get_object(request, pk)
        job.delete()
        messages.success(request, "Job offer deleted.")
        return redirect("core:jobs")


# Applications

class ApplyToJobView(LoginRequiredMixin, View):
    def post(self, request, pk):
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


class UpdateApplicationStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        application = get_object_or_404(JobApplication, pk=pk)
        if application.job.employer != request.user:
            return HttpResponseForbidden()
        new_status = request.POST.get("status")
        if new_status in [JobApplication.ACCEPTED, JobApplication.REJECTED, JobApplication.PENDING]:
            application.status = new_status
            application.save(update_fields=["status"])
            messages.success(request, f"Application marked as {new_status}.")
        return redirect("core:job-detail", pk=application.job.pk)


class MyApplicationsView(LoginRequiredMixin, ListView):
    model = JobApplication
    template_name = "core/my_applications.html"
    context_object_name = "applications"

    def get_queryset(self):
        return (
            JobApplication.objects
            .filter(freelancer=self.request.user)
            .select_related("job", "job__employer")
            .order_by("-created_at")
        )


#Messages

class InboxView(LoginRequiredMixin, TemplateView):
    template_name = "core/inbox.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        partner_ids = Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).values_list("sender_id", "receiver_id")

        ids = set()
        for s, r in partner_ids:
            ids.add(s)
            ids.add(r)
        ids.discard(user.pk)

        partners = User.objects.filter(pk__in=ids)
        ctx["partners"] = partners
        ctx["unread_counts"] = {
            p.pk: Message.objects.filter(sender=p, receiver=user, is_read=False).count()
            for p in partners
        }
        return ctx


class ConversationView(LoginRequiredMixin, View):
    template_name = "core/conversation.html"

    def get(self, request, user_id):
        return self._render(request, user_id)

    def post(self, request, user_id):
        other = get_object_or_404(User, pk=user_id)
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = other
            msg.save()
        return redirect("core:conversation", user_id=user_id)

    def _render(self, request, user_id):
        from django.shortcuts import render
        other = get_object_or_404(User, pk=user_id)
        msgs = Message.objects.filter(
            Q(sender=request.user, receiver=other) |
            Q(sender=other, receiver=request.user)
        ).order_by("created_at")
        msgs.filter(sender=other, is_read=False).update(is_read=True)
        return render(request, self.template_name, {
            "messages_qs": msgs,
            "other": other,
            "form": MessageForm(),
        })



class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        reviewee = get_object_or_404(User, pk=user_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewee = reviewee
            review.save()
            messages.success(request, "Review submitted!")
        return redirect(request.META.get("HTTP_REFERER", "core:home"))
