# Generated by Django 2.0.2 on 2018-02-18 21:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0011_auto_20180218_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badge',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='hybridbadges', to=settings.AUTH_USER_MODEL),
        ),
    ]