# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=255)),
                ('file_id', models.CharField(max_length=255)),
                ('folder', models.ForeignKey(to='secure_witness.Folder')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
