from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.models import (
    User, Skill, FreelancerProfile, EmployerProfile,
    JobOffer, JobApplication, Message, Review,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "role", "is_staff", "date_joined")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("WorkForge", {"fields": ("role", "avatar")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("WorkForge", {"fields": ("role",)}),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "experience_level", "years_experienced", "hourly_rate", "rating", "completed_projects")
    list_filter = ("experience_level",)
    search_fields = ("user__username", "user__email")
    filter_horizontal = ("skills",)


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name", "page_views")
    search_fields = ("user__username", "company_name")


@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = ("title", "employer", "budget", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "employer__username")
    filter_horizontal = ("skills_required",)
    date_hierarchy = "created_at"


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("freelancer", "job", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("freelancer__username", "job__title")
    date_hierarchy = "created_at"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "is_read", "created_at")
    list_filter = ("is_read",)
    search_fields = ("sender__username", "receiver__username")
    date_hierarchy = "created_at"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("reviewer", "reviewee", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("reviewer__username", "reviewee__username")
    date_hierarchy = "created_at"
