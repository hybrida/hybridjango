# Generated by Django 2.0.8 on 2018-10-23 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staticpages', '0019_auto_20181023_1908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boardreportsemester',
            name='semseter',
        ),
        migrations.AddField(
            model_name='boardreportsemester',
            name='semester',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='boardreportsemester',
            name='year',
            field=models.IntegerField(default=0),
        ),
    ]
