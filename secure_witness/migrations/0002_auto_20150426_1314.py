# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='activation_key',
            field=models.CharField(max_length=40, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 26, 17, 14, 13, 710412, tzinfo=utc)),
        ),
    ]
