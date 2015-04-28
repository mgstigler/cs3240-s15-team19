# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0010_media_filetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='iv',
            field=models.CharField(max_length=200, default=0),
        ),
        migrations.AlterField(
            model_name='media',
            name='key',
            field=models.CharField(max_length=200, default=0),
        ),
    ]
