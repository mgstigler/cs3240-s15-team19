# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0008_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='today',
        ),
        migrations.AlterField(
            model_name='report',
            name='time',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
