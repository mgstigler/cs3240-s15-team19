from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Keyword(models.Model):
    word = models.CharField(max_length=50)

class Report(models.Model):
    time = models.DateTimeField(auto_now=True)
    short = models.CharField(max_length=200)
    detailed = models.CharField(max_length=1000)
    location = models.CharField(max_length=50)
    date = models.CharField(max_length=1000)
    #keywords = models.CharField(max_length=1000)
    private = models.BooleanField(default=False)
    keywords = models.ManyToManyField(Keyword)

    def __str__(self):
       ''.join([self.short, self.detailed])


class UserProfile(models.Model):
    # Link UserProfile to an instance of User
    user = models.OneToOneField(User)

    # Extra fields aside from default user fields
    # TODO Add extra fields if needed

    def __str__(self):
        return self.user.username

