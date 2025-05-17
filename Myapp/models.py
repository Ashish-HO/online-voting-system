from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils import timezone

from datetime import date, timedelta
import uuid


# Create your models here.
class Voter(models.Model):
    voter = models.OneToOneField(to=User, on_delete=models.CASCADE)
    is_voted = models.BooleanField(default=False)
    voted_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.voter.username


class Candidate(models.Model):
    name = models.CharField(max_length=255)
    photo = models.TextField()
    phone = models.IntegerField()
    email = models.EmailField()
    description = models.TextField()
    votes = models.IntegerField(default=0, editable=False)
    post = models.ForeignKey(to="Post", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class ElectionSetting(models.Model):
    title = models.CharField(max_length=255)
    startdate = models.DateTimeField(
        default=timezone.now().date() + timedelta(days=1),
        # validators=[validate_startdate_in_future],
    )
    enddate = models.DateTimeField(default=date.today() + timedelta(days=2))

    def __str__(self):
        return self.title


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        """Check if token is still valid (e.g., expires in 1 hour)"""
        return timezone.now() - self.created_at < timedelta(hours=1)
