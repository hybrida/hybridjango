# Generated by Django 2.0.8 on 2019-10-16 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0017_hybrid_accepted_conditions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hybrid',
            name='specialization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.Specialization', verbose_name='Spesialisering'),
        ),
    ]
