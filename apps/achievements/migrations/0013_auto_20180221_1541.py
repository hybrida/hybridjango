# Generated by Django 2.0.2 on 2018-02-21 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0012_auto_20180218_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badge',
            name='badge_image',
            field=models.ImageField(upload_to='badges'),
        ),
    ]
