# Generated by Django 2.0.8 on 2019-01-29 09:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0011_auto_20190128_1344'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrontpageImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateField(default=datetime.datetime(2019, 1, 29, 9, 23, 20, 151465, tzinfo=utc)),
        ),
    ]
