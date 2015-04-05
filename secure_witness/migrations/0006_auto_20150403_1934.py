# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0005_auto_20150403_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='folder_id',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='folder',
            name='folder_name',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
    ]
