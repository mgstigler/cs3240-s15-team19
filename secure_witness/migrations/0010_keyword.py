# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0009_auto_20150410_2315'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('keywords', models.CharField(max_length=100, null=True, default='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
