# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-12 16:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bedkom', '0018_auto_20170912_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='responsible',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]