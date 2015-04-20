# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('secure_witness', '0003_auto_20150418_0321'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='authorized_groups',
            field=models.ManyToManyField(blank=True, to='auth.Group'),
            preserve_default=True,
        ),
    ]
