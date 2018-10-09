# Generated by Django 2.0.8 on 2018-10-02 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0017_hybrid_accepted_conditions'),
        ('bedkom', '0021_meetingreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='relevant_spesializations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='registration.Specialization'),
        ),
    ]
