# Generated by Django 2.0.8 on 2019-11-08 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0019_rename_badgeforslag'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='badge',
            options={'ordering': ['-weight', '-scorepoints']},
        ),
        migrations.AddField(
            model_name='badge',
            name='weight',
            field=models.PositiveIntegerField(default=10),
        ),
    ]