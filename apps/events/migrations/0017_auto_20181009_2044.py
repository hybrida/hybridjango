# Generated by Django 2.0.8 on 2018-10-09 18:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_mark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mark',
            name='start',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='mark',
            name='value',
            field=models.IntegerField(),
        ),
    ]
