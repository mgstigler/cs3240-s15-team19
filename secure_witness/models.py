from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    # Link UserProfile to an instance of User
    user = models.OneToOneField(User)

    # Extra fields aside from default user fields
    # TODO Add extra fields if needed

    def __str__(self):
        return self.user.username