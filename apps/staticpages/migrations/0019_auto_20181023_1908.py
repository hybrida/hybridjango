# Generated by Django 2.0.8 on 2018-10-23 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staticpages', '0018_auto_20181023_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardReportSemester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semseter', models.CharField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='boardreport',
            name='semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='staticpages.BoardReportSemester'),
        ),
    ]
