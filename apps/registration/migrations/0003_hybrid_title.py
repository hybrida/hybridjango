# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 23:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('registration', '0002_auto_20161029_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='hybrid',
            name='title',
            field=models.CharField(blank=True, default='Hybrid', max_length=150),
        ),
    ]