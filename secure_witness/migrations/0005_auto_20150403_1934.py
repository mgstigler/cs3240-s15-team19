# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0004_auto_20150403_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='folder',
            field=models.ForeignKey(to='secure_witness.Folder', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='folder',
            name='folder_id',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='folder',
            name='folder_name',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
