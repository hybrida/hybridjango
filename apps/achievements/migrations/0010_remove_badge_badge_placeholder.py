# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-10 07:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0009_auto_20180109_2238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badge',
            name='badge_placeholder',
        ),
    ]