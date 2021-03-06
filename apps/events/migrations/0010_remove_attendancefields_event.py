# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 14:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0009_add_attendance_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='genders',
        ),
        migrations.RemoveField(
            model_name='event',
            name='grades',
        ),
        migrations.RemoveField(
            model_name='event',
            name='max_participants',
        ),
        migrations.RemoveField(
            model_name='event',
            name='participants',
        ),
        migrations.RemoveField(
            model_name='event',
            name='price',
        ),
        migrations.RemoveField(
            model_name='event',
            name='signup_end',
        ),
        migrations.RemoveField(
            model_name='event',
            name='signup_start',
        ),
        migrations.RemoveField(
            model_name='event',
            name='waiting_list',
        ),
    ]
