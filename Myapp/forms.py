from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

from . import models


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# class CandidateAddForm(forms.ModelForm):
#     class Meta:
#         model = models.Candidate
#         field = ["name", "photo", "phone", "email", "description", "post"]


# class PostAddForm(forms.ModelForm):
#     class Meta:
#         model = models.Post
#         field = ["title", "description"]



