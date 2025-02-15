from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.

from . import models

# core/urls.py

admin.site.site_title = "Online voting systemsite admin"
admin.site.site_header = "Online Voting System Administration"
admin.site.index_title = "Site Administration"
admin.site.site_url = "/"
admin.site.enable_nav_sidebar = True
admin.site.empty_value_display = "-"

admin.site.register(models.Post)
admin.site.register(models.ElectionSetting)


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
