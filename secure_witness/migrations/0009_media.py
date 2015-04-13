# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0008_auto_20150405_1822'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('filename', models.CharField(max_length=200)),
                ('is_encrypted', models.BooleanField(default=True)),
                ('content', models.FileField(upload_to='')),
                ('report', models.ForeignKey(to='secure_witness.File')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
