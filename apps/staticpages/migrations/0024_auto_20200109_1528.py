# Generated by Django 2.0.8 on 2020-01-09 14:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('staticpages', '0023_auto_20200109_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, null=True),
        ),
    ]
