# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-09-05 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bedkom', '0016_auto_20170328_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='status',
            field=models.CharField(choices=[('Booket', 'Booket'), ('Opprettet kontakt', 'Opprettet kontakt'), ('Takket nei', 'Takket nei'), ('Ikke kontaktet', 'Ikke kontaktet'), ('Svarer ikke', 'Svarer ikke')], max_length=20),
        ),
    ]
