from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.

from . import models

admin.site.register(models.Post)


@admin.register(models.Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ["name", "post", "votes"]
    list_filter = ["post"]
    ordering = ["votes", "name"]


@admin.register(models.Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ["voter", "is_voted"]
    list_filter = ["is_voted"]
    ordering = ["voter", "is_voted"]
