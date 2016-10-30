# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 17:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('contact_person', models.CharField(max_length=150)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
                ('info', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.CharField(blank=True, max_length=400, null=True)),
                ('telephone', models.CharField(blank=True, max_length=30, null=True)),
                ('notes', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(choices=[('Booket', 'BOOKET'), ('Opprettet kontaktet', 'KONTAKTET'), ('Takket nei', 'NEI'), ('Ikke kontaktet', 'IKKE_KONTAKTET'), ('Sendt mail', 'SENDT_MAIL')], max_length=20)),
                ('priority', models.CharField(choices=[('Høy', 'HØY'), ('Middels', 'MIDDELS'), ('Lav', 'LAV')], max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='EarlierBedpresses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(blank=True, max_length=25, null=True)),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bedkom.Company')),
            ],
        ),
    ]
