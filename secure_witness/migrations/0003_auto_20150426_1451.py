# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0002_auto_20150426_1314'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('basemodel_ptr', models.OneToOneField(serialize=False, primary_key=True, to='secure_witness.BaseModel', parent_link=True, auto_created=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('report', models.ForeignKey(to='secure_witness.Report')),
            ],
            bases=('secure_witness.basemodel',),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 26, 18, 51, 12, 215219, tzinfo=utc)),
        ),
    ]
