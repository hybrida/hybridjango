# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-10-10 11:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0012_add_timestamp_ordering_participation'),
        ('rfid', '0002_auto_20171002_1714'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralAssembly',
            fields=[
                ('event', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='events.Event')),
                ('users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
