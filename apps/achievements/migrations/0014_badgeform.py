# Generated by Django 2.0.3 on 2018-03-21 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0013_auto_20180221_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='BadgeForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('badge_image', models.ImageField(upload_to='badges')),
                ('scorepoints', models.PositiveIntegerField()),
            ],
        ),
    ]
