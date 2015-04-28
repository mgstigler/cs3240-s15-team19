# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0009_auto_20150427_0502'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='fileType',
            field=models.CharField(max_length=200, default=''),
        ),
    ]
