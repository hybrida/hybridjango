# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-24 18:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bedkom', '0007_remove_company_telephone'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_person',
            name='job',
            field=models.CharField(default='hei', max_length=100),
        ),
        migrations.AddField(
            model_name='contact_person',
            name='telephone',
            field=models.CharField(default='99253420', max_length=50),
        ),
    ]
