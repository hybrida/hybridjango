# Generated by Django 2.0.8 on 2019-12-06 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0023_auto_20191206_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='code',
            field=models.CharField(max_length=10, unique=True, verbose_name='Fagkode'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Fagnavn'),
        ),
    ]
