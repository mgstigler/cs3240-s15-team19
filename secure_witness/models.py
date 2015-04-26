from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.utils import timezone


class BaseModel(models.Model):
    """
    Base class to hold meta data about other models
    """
    created_by = models.ForeignKey(User, related_name='created_by', editable=False)
    updated_by = models.ForeignKey(User, related_name='updated_by', editable=False)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

    # Override the save function to store the date
    # Do this instead of auto_created, etc. for better reliability
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)

class Folder(BaseModel):

    folder_name = models.CharField(
        max_length=255, null=True
    )

    def get_absolute_url(self):

        return reverse('folders-view', kwargs={'pk': self.id})


    def __str__(self):

        return self.folder_name

class Keyword(models.Model):
   keywords = models.CharField(max_length=100, default='', null=True)

class Report(BaseModel):
    folder = models.ForeignKey(Folder, null=True)
    time = models.DateField(max_length=50, null=True)
    short = models.CharField(max_length=200, default='', null=True)
    detailed = models.CharField(max_length=1000, default='', null=True)
    location = models.CharField(max_length=50, default='', null=True)
    today = models.CharField(max_length=1000, default='', null=True)
    keywords = models.CharField(max_length=1000, default='', null=True)
    #KWset = models.ManyToManyField(Keyword)
    private = models.BooleanField(default=False)
    authorized_groups = models.ManyToManyField(Group, blank=True)

    def __str__(self):

        return ' '.join([
            self.short,
            self.detailed,
        ])

class Media(BaseModel):
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
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.user.username


