# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-24 19:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bedkom', '0008_auto_20170124_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='contact_person',
        ),
        migrations.AddField(
            model_name='contact_person',
            name='company',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bedkom.Company'),
        ),
    ]
