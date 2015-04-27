# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0005_auto_20150427_0313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 27, 3, 36, 44, 923949, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
