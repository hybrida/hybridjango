# Generated by Django 2.0.8 on 2018-10-30 20:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kiltshop', '0001_initial_squashed_0015_remove_orderinfo_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]