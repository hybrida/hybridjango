# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-02 12:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0013_auto_20171002_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hybrid',
            name='card_key',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='NTNU-kortkode'),
        ),
    ]