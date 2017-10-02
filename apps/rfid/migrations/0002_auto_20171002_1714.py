# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-10-02 15:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rfid', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appearances',
            name='id',
        ),
        migrations.AlterField(
            model_name='appearances',
            name='event',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='events.Event'),
        ),
    ]
