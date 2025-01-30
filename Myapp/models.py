from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Voter(models.Model):
    voter = models.OneToOneField(to=User, on_delete=models.CASCADE)
    is_voted = models.BooleanField(default=False)
    voted_time = models.DateTimeField(auto_now=True)


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


 
