# Generated by Django 2.0.4 on 2018-04-25 09:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staticpages', '0013_auto_20180424_2315'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ComApplication',
            new_name='CommiteApplication',
        ),
    ]
