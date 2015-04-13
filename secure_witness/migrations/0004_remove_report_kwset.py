# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0003_auto_20150412_2319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='KWset',
        ),
    ]
