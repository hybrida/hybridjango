# Generated by Django 2.0.4 on 2018-05-04 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vevkom', '0003_auto_20180411_1837'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meetingreport',
            old_name='people',
            new_name='tilstede',
        ),
    ]
