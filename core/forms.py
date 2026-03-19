from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.models import (
    User,
    FreelancerProfile,
    EmployerProfile,
    JobOffer,
    JobApplication,
    Message,
    Review,
)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "avatar",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

        self.fields["avatar"].required = False


class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = [
            "bio",
            "experience_level",
            "years_experienced",
            "hourly_rate",
            "skills",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "experience_level": forms.TextInput(attrs={"class": "form-control"}),
            "years_experienced": forms.NumberInput(attrs={"class": "form-control"}),
            "hourly_rate": forms.NumberInput(attrs={"class": "form-control"}),
            "skills": forms.CheckboxSelectMultiple(),
        }


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ["bio", "company_name"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class JobOfferForm(forms.ModelForm):
    class Meta:
        model = JobOffer
        fields = ["title", "description", "budget", "skills_required", "status"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 5, "class": "form-control"}),
            "budget": forms.NumberInput(attrs={"class": "form-control"}),
            "skills_required": forms.CheckboxSelectMultiple(),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ["cover_letter"]
        widgets = {
            "cover_letter": forms.Textarea(
                attrs={
                    "rows": 6,
                    "class": "form-control",
                    "placeholder": "Tell the employer why you are the best fit…",
                }
            )
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Write a message…",
                }
            )
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "max": 5}
            ),
            "comment": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }


class AvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar"]
        widgets = {
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"})
        }