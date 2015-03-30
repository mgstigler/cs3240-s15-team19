from django.db import models

# Create your models here.
class Keyword(models.Model):
    word = models.CharField(max_length=50)

class Report(models.Model):
    time = models.DateTimeField(auto_now=True)
    short = models.CharField(max_length=200)
    detailed = models.CharField(max_length=1000)
    location = models.CharField(max_length=50)
    date = models.CharField(max_length=1000)
    keywords = models.CharField(max_length=1000)
    private = models.BooleanField(default=False)
    #keywords = models.ManyToManyField(Keyword)

