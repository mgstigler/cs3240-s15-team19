# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='keywords',
            field=models.ManyToManyField(to='secure_witness.Keyword'),
            preserve_default=True,
        ),
    ]
