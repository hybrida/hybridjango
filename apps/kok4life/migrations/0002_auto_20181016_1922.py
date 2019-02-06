# Generated by Django 2.0.8 on 2018-10-16 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kok4life', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('file', models.FileField(upload_to='kok')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='subjects',
            name='subject',
        ),
        migrations.DeleteModel(
            name='Files',
        ),
        migrations.DeleteModel(
            name='Subjects',
        ),
        migrations.AddField(
            model_name='file',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kok4life.Subject'),
        ),
    ]