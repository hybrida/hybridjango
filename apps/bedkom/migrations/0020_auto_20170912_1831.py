# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-12 16:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bedkom', '0019_auto_20170912_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='info',
            field=models.CharField(blank=True, help_text='Hvem er bedriften, hva gjør de og hvilke fagområder er de involvert i?', max_length=300, null=True),
        ),
    ]
