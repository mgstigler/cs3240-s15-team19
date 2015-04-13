# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secure_witness', '0002_auto_20150402_1439'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('filename', models.CharField(max_length=200)),
                ('is_encrypted', models.BooleanField(default=True)),
                ('content', models.FileField(upload_to='')),
                ('report', models.ForeignKey(to='secure_witness.Report')),
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
        migrations.RemoveField(
            model_name='keyword',
            name='word',
        ),
        migrations.AddField(
            model_name='keyword',
            name='keywords',
            field=models.CharField(null=True, max_length=100, default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='KWset',
            field=models.ManyToManyField(to='secure_witness.Keyword'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='keywords',
            field=models.CharField(null=True, max_length=1000, default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='today',
            field=models.CharField(null=True, max_length=1000, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='folder',
            name='folder_id',
            field=models.CharField(null=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='folder',
            name='folder_name',
            field=models.CharField(null=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='detailed',
            field=models.CharField(null=True, max_length=1000, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='location',
            field=models.CharField(null=True, max_length=50, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='short',
            field=models.CharField(null=True, max_length=200, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='time',
            field=models.CharField(null=True, max_length=50, default=''),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='report',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='report',
            name='date',
        ),
    ]
