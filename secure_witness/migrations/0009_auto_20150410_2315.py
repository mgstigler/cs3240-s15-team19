# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0008_auto_20150405_1822'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('time', models.CharField(max_length=50, default='', null=True)),
                ('short', models.CharField(max_length=200, default='', null=True)),
                ('detailed', models.CharField(max_length=1000, default='', null=True)),
                ('location', models.CharField(max_length=50, default='', null=True)),
                ('today', models.CharField(max_length=1000, default='', null=True)),
                ('keywords', models.CharField(max_length=1000, default='', null=True)),
                ('private', models.BooleanField(default=False)),
                ('folder', models.ForeignKey(to='secure_witness.Folder')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='file',
            name='folder',
        ),
        migrations.DeleteModel(
            name='File',
        ),
    ]
