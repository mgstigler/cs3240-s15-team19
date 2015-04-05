# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0002_auto_20150403_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='detailed',
            field=models.CharField(default=b'', max_length=1000, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='keywords',
            field=models.CharField(default=b'', max_length=1000, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='location',
            field=models.CharField(default=b'', max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='short',
            field=models.CharField(default=b'', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='time',
            field=models.CharField(default=b'', max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='today',
            field=models.CharField(default=b'', max_length=1000, null=True),
            preserve_default=True,
        ),
    ]
