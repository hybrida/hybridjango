# Generated by Django 2.0.8 on 2020-02-11 22:59

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0038_auto_20200130_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_end',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Slutt'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_start',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Start'),
        ),
        migrations.AlterField(
            model_name='event',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name='Utkast'),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, upload_to='events', verbose_name='Bilde'),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(blank=True, max_length=50, verbose_name='Sted'),
        ),
        migrations.AlterField(
            model_name='event',
            name='news',
            field=models.BooleanField(default=True, verbose_name='Nyhet'),
        ),
        migrations.AlterField(
            model_name='event',
            name='public',
            field=models.BooleanField(default=True, verbose_name='Synlig for alle'),
        ),
        migrations.AlterField(
            model_name='event',
            name='signoff_close',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, verbose_name='Antall timer før hendelsen starter avmeldingen skal stenge'),
        ),
        migrations.AlterField(
            model_name='event',
            name='signoff_close_on_signup_close',
            field=models.BooleanField(default=False, verbose_name='Steng avmelding når påmeldingen stenger'),
        ),
        migrations.AlterField(
            model_name='event',
            name='text',
            field=tinymce.models.HTMLField(blank=True, verbose_name='Tekst'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Tittel'),
        ),
        migrations.AlterField(
            model_name='event',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='Vekting'),
        ),
    ]
