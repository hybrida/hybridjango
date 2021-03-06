# Generated by Django 2.0.8 on 2018-11-16 23:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0007_auto_20181116_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='sum',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateField(default=datetime.datetime(2018, 11, 16, 23, 47, 47, 897715, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
