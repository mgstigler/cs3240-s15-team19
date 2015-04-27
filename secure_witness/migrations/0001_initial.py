# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, to='secure_witness.BaseModel', serialize=False)),
                ('folder_name', models.CharField(null=True, max_length=255)),
            ],
            options={
            },
            bases=('secure_witness.basemodel',),
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('keywords', models.CharField(null=True, default='', max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, to='secure_witness.BaseModel', serialize=False)),
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
                ('basemodel_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, to='secure_witness.BaseModel', serialize=False)),
                ('time', models.DateField(null=True, max_length=50)),
                ('short', models.CharField(null=True, default='', max_length=200)),
                ('detailed', models.CharField(null=True, default='', max_length=1000)),
                ('location', models.CharField(null=True, default='', max_length=50)),
                ('today', models.CharField(null=True, default='', max_length=1000)),
                ('keywords', models.CharField(null=True, default='', max_length=1000)),
                ('private', models.BooleanField(default=False)),
                ('authorized_groups', models.ManyToManyField(to='auth.Group', blank=True)),
                ('folder', models.ForeignKey(null=True, to='secure_witness.Folder')),
            ],
            options={
            },
            bases=('secure_witness.basemodel',),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
            field=models.ForeignKey(editable=False, related_name='created_by', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='basemodel',
            name='updated_by',
            field=models.ForeignKey(editable=False, related_name='updated_by', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
