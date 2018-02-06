# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 21:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('staticpages', '0004_auto_20170321_2001'),
    ]

    operations = [
        migrations.CreateModel(
            name='Protocol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protocol', models.FileField(upload_to='pdf/protokoll')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('description', models.CharField(blank=True, max_length=50)),
            ],
        ),
    ]
