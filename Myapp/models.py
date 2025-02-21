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
    votes = models.IntegerField(default=0, editable=True)
    post = models.ForeignKey(to="Post", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


# validator for start date of election settings
# def validate_startdate_in_future(value):
#     if value <= timezone.now().date():
#         raise ValidationError("The start date must be in the future.")


class ElectionSetting(models.Model):
    title = models.CharField(max_length=255)
    startdate = models.DateField(
        default=timezone.now().date() + timedelta(days=1),
        # validators=[validate_startdate_in_future],
    )
    enddate = models.DateField(default=date.today() + timedelta(days=2))

    # # validation for end date
    # def clean(self):
    #     super().clean()
    #     if self.enddate <= self.startdate:
    #         raise ValidationError("The end date must be after the start date.")

    # def save(self, *args, **kwargs):
    #     self.full_clean()  # This will call the clean method
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        """Check if token is still valid (e.g., expires in 1 hour)"""
        return now() - self.created_at < timedelta(hours=1)
