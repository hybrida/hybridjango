# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('registration', '0004_switch_specialization_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialization',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
