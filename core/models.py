from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_FREELANCER = "freelancer"
    ROLE_EMPLOYER = "employer"
    ROLE_CHOICES  = [
        (ROLE_FREELANCER, "Freelancer"),
        (ROLE_EMPLOYER, "Employer"),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_FREELANCER
    )
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def is_freelancer(self):
        return self.role == self.ROLE_FREELANCER

    @property
    def is_employer(self):
        return self.role == self.ROLE_EMPLOYER

    @property
    def get_user(self):
        return self.get_full_name()

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FreelancerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    skills = models.ManyToManyField(Skill, blank=True)
    bio = models.TextField(blank=True)
    experience_level = models.CharField(max_length=10, blank=True)
    years_experienced = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    completed_projects = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} - freelancer"


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    page_views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - employer"


class JobOffer(models.Model):
    OPEN = "open"
    CLOSED = "closed"
    employer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="job_offers",
    )
    title   = models.CharField(max_length=200)
    description = models.TextField()
    skills_required = models.ManyToManyField(Skill, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[
            (OPEN, "Open"),
            (CLOSED, "Closed")
        ], default="open")

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    job = models.ForeignKey(JobOffer, on_delete=models.CASCADE, related_name="applications")
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=[
            (PENDING, "Pending"),
            (ACCEPTED, "Accepted"),
            (REJECTED, "Rejected"),
        ],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.freelancer.username} -> {self.job.title}"



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_given")
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_received")
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer} -> {self.reviewee}: {self.rating}"
