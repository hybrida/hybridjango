# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-25 19:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0011_participation_excursion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participation',
            options={'ordering': ['timestamp']},
        ),
    ]
