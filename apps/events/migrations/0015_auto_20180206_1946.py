# Generated by Django 2.0.2 on 2018-02-06 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20171102_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='specializations',
            field=models.ManyToManyField(blank=True, limit_choices_to={'active': True}, to='registration.Specialization'),
        ),
    ]
