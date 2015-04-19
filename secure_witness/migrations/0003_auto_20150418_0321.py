# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0002_auto_20150402_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basemodel',
            name='created_by',
            field=models.ForeignKey(editable=False, related_name='created_by', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basemodel',
            name='updated_at',
            field=models.DateTimeField(editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basemodel',
            name='updated_by',
            field=models.ForeignKey(editable=False, related_name='updated_by', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
