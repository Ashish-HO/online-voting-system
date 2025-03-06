from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

from . import models


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CandidateAddForm(forms.ModelForm):
    post = forms.ModelChoiceField(
        queryset=models.Post.objects.all(), empty_label="select post"
    )

    class Meta:
        model = models.Candidate
        fields = "__all__"


class PostAddForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ["name", "description"]


class ElectionForm(forms.ModelForm):
    class Meta:
        model = models.ElectionSetting
        fields = "__all__"
