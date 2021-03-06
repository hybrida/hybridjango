# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 17:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('ingress', models.CharField(blank=True, max_length=500)),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(default='placeholder-event.png', upload_to='events')),
                ('max_participants', models.IntegerField(default=0)),
                ('price', models.PositiveIntegerField(default=0)),
                ('location', models.CharField(blank=True, max_length=50)),
                ('signup_start', models.DateTimeField(blank=True, null=True)),
                ('signup_end', models.DateTimeField(blank=True, null=True)),
                ('event_start', models.DateTimeField(blank=True, null=True)),
                ('event_end', models.DateTimeField(blank=True, null=True)),
                ('weight', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='EventComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField()),
            ],
        ),
    ]
