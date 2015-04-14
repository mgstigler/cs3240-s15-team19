from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Folder(models.Model):

    folder_name = models.CharField(
        max_length=255, null=True
    )

    def get_absolute_url(self):

        return reverse('folders-view', kwargs={'pk': self.id})


    def __str__(self):

        return self.folder_name

class Keyword(models.Model):
   keywords = models.CharField(max_length=100, default='', null=True)

class Report(models.Model):
    folder = models.ForeignKey(Folder, null=True)
    time = models.DateField(max_length=50, null=True)
    short = models.CharField(max_length=200, default='', null=True)
    detailed = models.CharField(max_length=1000, default='', null=True)
    location = models.CharField(max_length=50, default='', null=True)
    today = models.CharField(max_length=1000, default='', null=True)
    keywords = models.CharField(max_length=1000, default='', null=True)
    #KWset = models.ManyToManyField(Keyword)
    private = models.BooleanField(default=False)



    def __str__(self):

        return ' '.join([
            self.short,
            self.detailed,
        ])

class Media(models.Model):
    filename = models.CharField(max_length=200)
    is_encrypted = models.BooleanField(default=True)
    content = models.FileField()
    report = models.ForeignKey('Report')
    key = models.CharField(max_length=200)
    iv = models.CharField(max_length=200)

    def __str__(self):
        return self.filename

class UserProfile(models.Model):
    # Link UserProfile to an instance of User
    user = models.OneToOneField(User)

    # Extra fields aside from default user fields
    # TODO Add extra fields if needed

    def __str__(self):
        return self.user.username


