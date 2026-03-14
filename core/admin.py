from django.contrib import admin

from core.models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass

@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    pass

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
