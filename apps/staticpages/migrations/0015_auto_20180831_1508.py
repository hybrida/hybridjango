# Generated by Django 2.0.4 on 2018-08-31 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staticpages', '0014_auto_20180425_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='comment',
            field=models.TextField(blank=True, max_length=5000),
        ),
        migrations.AddField(
            model_name='application',
            name='granted',
            field=models.CharField(blank=True, choices=[('Støttet', 'Støttet'), ('Delvis støttet', 'Delvis støttet'), ('Ikke støttet', 'Ikke støttet')], max_length=500),
        ),
    ]
