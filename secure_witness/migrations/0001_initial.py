# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('keywords', models.CharField(max_length=100, default='', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, to='secure_witness.BaseModel', primary_key=True, serialize=False, parent_link=True)),
                ('folder_name', models.CharField(max_length=255, null=True)),
            ],
            bases=('secure_witness.basemodel',),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, to='secure_witness.BaseModel', primary_key=True, serialize=False, parent_link=True)),
                ('filename', models.CharField(max_length=200)),
                ('is_encrypted', models.BooleanField(default=True)),
                ('content', models.FileField(upload_to='')),
                ('key', models.CharField(max_length=200)),
                ('iv', models.CharField(max_length=200)),
            ],
            bases=('secure_witness.basemodel',),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, to='secure_witness.BaseModel', primary_key=True, serialize=False, parent_link=True)),
                ('time', models.DateField(max_length=50, null=True)),
                ('short', models.CharField(max_length=200, default='', null=True)),
                ('detailed', models.CharField(max_length=1000, default='', null=True)),
                ('location', models.CharField(max_length=50, default='', null=True)),
                ('today', models.CharField(max_length=1000, default='', null=True)),
                ('keywords', models.CharField(max_length=1000, default='', null=True)),
                ('private', models.BooleanField(default=False)),
                ('authorized_groups', models.ManyToManyField(blank=True, to='auth.Group')),
                ('folder', models.ForeignKey(to='secure_witness.Folder', null=True)),
            ],
            bases=('secure_witness.basemodel',),
        ),
        migrations.AddField(
            model_name='basemodel',
            name='created_by',
            field=models.ForeignKey(editable=False, related_name='created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='basemodel',
            name='updated_by',
            field=models.ForeignKey(editable=False, related_name='updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='media',
            name='report',
            field=models.ForeignKey(to='secure_witness.Report'),
        ),
    ]
