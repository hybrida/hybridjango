# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-03-16 12:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BoardReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.FileField(upload_to='static/pdf/møtereferat')),
                ('date', models.DateField(default=datetime.date(2017, 3, 16))),
            ],
        ),
    ]