# Generated by Django 2.0.8 on 2019-01-29 09:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0013_auto_20190129_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateField(default=datetime.datetime(2019, 1, 29, 9, 53, 1, 713940, tzinfo=utc)),
        ),
    ]