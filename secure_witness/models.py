from django.core.exceptions import ValidationError
from django.db import models
from django.core.urlresolvers import reverse


class Folder(models.Model):

    folder_name = models.CharField(
        max_length=255,
    )
    folder_id = models.CharField(
        max_length=255,

    )

    def get_absolute_url(self):

        return reverse('folders-view', kwargs={'pk': self.id})


    def __str__(self):

        return ' '.join([
            self.folder_name,
            self.folder_id,
        ])

class File(models.Model):
    folder = models.ForeignKey(Folder)
    file_name = models.CharField(
        max_length=255,
    )
    file_id = models.CharField(
        max_length=255,

    )

    def __str__(self):

        return ' '.join([
            self.file_name,
            self.file_id,
        ])