# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-15 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20161108_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
