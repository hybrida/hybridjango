# Generated by Django 2.0.3 on 2018-04-11 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vevkom', '0002_guide'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingreport',
            name='text',
            field=models.TextField(max_length=3000),
        ),
    ]