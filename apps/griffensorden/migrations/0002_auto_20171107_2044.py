# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-07 19:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('griffensorden', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ridder',
            name='name',
        ),
        migrations.AddField(
            model_name='ridder',
            name='hybrid',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
