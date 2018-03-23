# Generated by Django 2.0.3 on 2018-03-23 12:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CakeMaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number_on_list', models.IntegerField(unique=True)),
            ],
            options={
                'ordering': ['-number_on_list'],
            },
        ),
        migrations.CreateModel(
            name='MeetingReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('people', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=3000)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('responsible', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=3000)),
                ('status', models.CharField(choices=[('Påbegynt', 'Påbegynt'), ('Ikke Påbegynt', 'Ikke Påbegynt'), ('Ferdig', 'Ferdig')], max_length=100)),
                ('priority', models.CharField(choices=[('Høy', 'Høy'), ('Middels', 'Middels'), ('Lav', 'Lav')], max_length=100)),
            ],
        ),
    ]
