# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Keyword',
        ),
        migrations.AlterUniqueTogether(
            name='report',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='report',
            name='folder',
        ),
        migrations.DeleteModel(
            name='Report',
        ),
        migrations.RemoveField(
            model_name='file',
            name='file_id',
        ),
        migrations.RemoveField(
            model_name='file',
            name='file_name',
        ),
        migrations.AddField(
            model_name='file',
            name='detailed',
            field=models.CharField(default=b'', max_length=1000),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='keywords',
            field=models.CharField(default=b'', max_length=1000),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='location',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='short',
            field=models.CharField(default=b'', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='time',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='today',
            field=models.CharField(default=b'', max_length=1000),
            preserve_default=True,
        ),
    ]
