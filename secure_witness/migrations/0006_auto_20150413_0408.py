# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0005_auto_20150413_0406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='reporter',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
