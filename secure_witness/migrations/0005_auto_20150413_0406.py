# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('secure_witness', '0004_remove_report_kwset'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folder',
            name='folder_id',
        ),
        migrations.AddField(
            model_name='report',
            name='reporter',
            field=models.OneToOneField(default=b'', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
