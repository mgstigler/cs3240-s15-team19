import os
from django.db import migrations
from django.contrib.auth.models import Group, User
from django.core.management import call_command

fixture = 'initial_data'

def load_fixture(apps, schema_editor):
    call_command('loaddata', fixture, app_label='secure_witness')

def unload_fixture(apps, schema_editor):
    # Delete all entries
    Group.objects.all().delete()
    User.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('secure_witness', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture)
    ]