# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('basemodel_ptr', models.OneToOneField(primary_key=True, auto_created=True, serialize=False, to='secure_witness.BaseModel', parent_link=True)),
                ('folder_name', models.CharField(null=True, max_length=255)),
            ],
            options={
            },
            bases=('secure_witness.basemodel',),
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('keywords', models.CharField(null=True, max_length=100, default='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('basemodel_ptr', models.OneToOneField(primary_key=True, auto_created=True, serialize=False, to='secure_witness.BaseModel', parent_link=True)),
                ('filename', models.CharField(max_length=200)),
                ('is_encrypted', models.BooleanField(default=True)),
                ('content', models.FileField(upload_to='')),
                ('key', models.CharField(max_length=200)),
                ('iv', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=('secure_witness.basemodel',),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('basemodel_ptr', models.OneToOneField(primary_key=True, auto_created=True, serialize=False, to='secure_witness.BaseModel', parent_link=True)),
                ('time', models.DateField(null=True, max_length=50)),
                ('short', models.CharField(null=True, max_length=200, default='')),
                ('detailed', models.CharField(null=True, max_length=1000, default='')),
                ('location', models.CharField(null=True, max_length=50, default='')),
                ('today', models.CharField(null=True, max_length=1000, default='')),
                ('keywords', models.CharField(null=True, max_length=1000, default='')),
                ('private', models.BooleanField(default=False)),
                ('folder', models.ForeignKey(null=True, to='secure_witness.Folder')),
            ],
            options={
            },
            bases=('secure_witness.basemodel',),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='media',
            name='report',
            field=models.ForeignKey(to='secure_witness.Report'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='basemodel',
            name='created_by',
            field=models.ForeignKey(related_name='created_by', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='basemodel',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_by', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
